import re
import json
import logging
from datetime import datetime
from typing import Tuple, Dict, List
from transformers import pipeline
import torch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DetoxifyGuardrails:
    """
    Guardrails system for DetoxifyAI that validates inputs and moderates outputs.

    Input Validation Rules:
    1. PII Detection - Blocks personally identifiable information
    2. Prompt Injection Filter - Blocks manipulation attempts

    Output Moderation Rules:
    1. Toxicity Threshold - Ensures rephrased text is non-toxic
    2. Hallucination Filter - Blocks empty or nonsensical outputs
    """

    def __init__(self, toxicity_threshold: float = 0.3,
                 log_file: str = "guardrail_events.json"):
        """
        Initialize guardrails with validation rules and monitoring.

        Args:
            toxicity_threshold: Maximum acceptable toxicity score (0-1)
            log_file: Path to JSON file for logging guardrail events
        """
        self.toxicity_threshold = toxicity_threshold
        self.log_file = log_file
        self.events: List[Dict] = []

        # Input validation patterns
        self.pii_patterns = {
            'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            'credit_card': re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b')
        }

        # Prompt injection keywords (case-insensitive)
        self.prompt_injection_keywords = [
            'ignore previous instructions',
            'ignore all previous',
            'disregard previous',
            'system:',
            'admin:',
            'sudo',
            'act as',
            'pretend you are',
            'you are now',
            'new instructions:',
            'override instructions'
        ]

        # Initialize toxicity detector for output validation
        logger.info("Loading toxicity detection model...")
        device = 0 if torch.cuda.is_available() else -1
        device_name = "GPU" if device == 0 else "CPU"
        logger.info(f"Using device: {device_name}")

        self.toxicity_detector = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            device=device,
            top_k=None
        )
        logger.info("Guardrails initialized successfully")

    def validate_input(self, text: str) -> Tuple[bool, str, Dict]:
        """
        Validate input text before RAG processing.

        Args:
            text: User input text to validate

        Returns:
            Tuple of (is_valid, reason, metadata)
        """
        # Rule 1: PII Detection
        for pii_type, pattern in self.pii_patterns.items():
            matches = pattern.findall(text)
            if matches:
                self._log_event(
                    event_type='input_pii_blocked',
                    rule='pii_detection',
                    detail=f'{pii_type} detected',
                    text_sample=self._sanitize_pii(text, matches),
                    metadata={'pii_type': pii_type, 'count': len(matches)}
                )
                return False, f"PII detected: {pii_type}", {'rule': 'pii', 'pii_type': pii_type}

        # Rule 2: Prompt Injection Filter
        text_lower = text.lower()
        for keyword in self.prompt_injection_keywords:
            if keyword in text_lower:
                self._log_event(
                    event_type='input_injection_blocked',
                    rule='prompt_injection',
                    detail=f'Keyword: {keyword}',
                    text_sample=text[:100],
                    metadata={'keyword': keyword}
                )
                return False, "Potential prompt injection detected", {'rule': 'injection', 'keyword': keyword}

        # Rule 3: Length validation (prevent abuse)
        if len(text) > 500:
            self._log_event(
                event_type='input_length_exceeded',
                rule='length_limit',
                detail=f'Length: {len(text)} chars',
                text_sample=text[:100],
                metadata={'length': len(text)}
            )
            return False, "Input exceeds maximum length (500 chars)", {'rule': 'length', 'length': len(text)}

        if len(text.strip()) < 5:
            self._log_event(
                event_type='input_too_short',
                rule='length_limit',
                detail=f'Length: {len(text)} chars',
                text_sample=text,
                metadata={'length': len(text)}
            )
            return False, "Input too short (minimum 5 chars)", {'rule': 'length', 'length': len(text)}

        # All checks passed
        logger.info("Input validation passed")
        return True, "OK", {}

    def validate_output(self, text: str) -> Tuple[bool, str, Dict]:
        """
        Validate output text after RAG processing.
        Args:
            text: RAG-generated output text to validate

        Returns:
            Tuple of (is_valid, reason, metadata)
        """
        # Rule 1: Toxicity threshold check
        try:
            result = self.toxicity_detector(text)[0]
            # Find toxic label score
            toxicity_score = 0.0
            for item in result:
                if item['label'].lower() == 'toxic':
                    toxicity_score = item['score']
                    break

            if toxicity_score > self.toxicity_threshold:
                self._log_event(
                    event_type='output_toxicity_blocked',
                    rule='toxicity_threshold',
                    detail=f'Score: {toxicity_score:.3f}',
                    text_sample=text[:100],
                    metadata={'toxicity_score': toxicity_score, 'threshold': self.toxicity_threshold}
                )
                return False, f"Output toxicity too high ({toxicity_score:.3f})", {
                    'rule': 'toxicity',
                    'score': toxicity_score,
                    'threshold': self.toxicity_threshold
                }
        except Exception as e:
            logger.error(f"Error in toxicity detection: {e}")
            # Fail open (allow output) if toxicity detection fails
            toxicity_score = 0.0

        # Rule 2: Hallucination/empty output filter
        stripped_text = text.strip()
        if len(stripped_text) < 10:
            self._log_event(
                event_type='output_too_short',
                rule='hallucination_filter',
                detail=f'Length: {len(stripped_text)} chars',
                text_sample=text,
                metadata={'length': len(stripped_text)}
            )
            return False, "Output too short or empty", {'rule': 'empty', 'length': len(stripped_text)}

        # Check for repetitive output (possible hallucination)
        words = stripped_text.split()
        if len(words) > 5:
            unique_words = len(set(words))
            repetition_ratio = unique_words / len(words)
            if repetition_ratio < 0.3:  # More than 70% repeated words
                self._log_event(
                    event_type='output_repetitive',
                    rule='hallucination_filter',
                    detail=f'Repetition ratio: {repetition_ratio:.3f}',
                    text_sample=text[:100],
                    metadata={'repetition_ratio': repetition_ratio}
                )
                return False, "Output appears repetitive/hallucinated", {
                    'rule': 'hallucination',
                    'repetition_ratio': repetition_ratio
                }

        # All checks passed
        logger.info(f"Output validation passed (toxicity: {toxicity_score:.3f})")
        return True, "OK", {'toxicity_score': toxicity_score}

    def _sanitize_pii(self, text: str, matches: List[str]) -> str:
        """Replace PII matches with [REDACTED] for logging."""
        sanitized = text
        for match in matches:
            sanitized = sanitized.replace(match, '[REDACTED]')
        return sanitized[:100]

    def _log_event(self, event_type: str, rule: str, detail: str, text_sample: str, metadata: Dict):
        """Log a guardrail event for monitoring."""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'rule': rule,
            'detail': detail,
            'text_sample': text_sample,
            'metadata': metadata
        }
        self.events.append(event)
        logger.warning(f"Guardrail event: {event_type} - {detail}")

        # Write to log file
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(event) + '\n')
        except Exception as e:
            logger.error(f"Failed to write to log file: {e}")

    def get_events(self) -> List[Dict]:
        """Get all logged guardrail events."""
        return self.events

    def get_event_summary(self) -> Dict:
        """Get summary statistics of guardrail events."""
        if not self.events:
            return {
                'total_events': 0,
                'by_type': {},
                'by_rule': {}
            }

        event_types = {}
        rules = {}

        for event in self.events:
            # Count by event type
            event_type = event['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1

            # Count by rule
            rule = event['rule']
            rules[rule] = rules.get(rule, 0) + 1

        return {
            'total_events': len(self.events),
            'by_type': event_types,
            'by_rule': rules
        }

    def clear_events(self):
        """Clear all logged events (useful for testing)."""
        self.events = []
        logger.info("Cleared all guardrail events")
