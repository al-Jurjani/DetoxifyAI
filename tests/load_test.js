import http from "k6/http";
import { check, sleep } from "k6";
import { Trend } from "k6/metrics";

const BASE_URL = "http://localhost:8000"; // since running locally
const PREDICT_URL = `${BASE_URL}/predict`;

export let options = {
  vus: 10, // 10 virtual users
  duration: "30s", // test for 30 seconds
  thresholds: {
    http_req_duration: ["p(95)<500"], // 95% requests <500ms
    http_req_failed: ["rate<0.05"], // <5% failed
  },
};

let latency = new Trend("request_latency");

export default function () {
  const payload = JSON.stringify({
    text: "This is a horrible comment", // sample text
  });

  const headers = { "Content-Type": "application/json" };
  const res = http.post(PREDICT_URL, payload, { headers });

  latency.add(res.timings.duration);

  check(res, {
    "status is 200": (r) => r.status === 200,
    "has prediction field": (r) => r.json("prediction") !== undefined,
  });

  sleep(1);
}
