# Load Testing Notes


Load testing is necessary to identify performance bottlenecks by using high-scale load tests.

## Table of Contents

1. Load testing basic
2. Nexis K8s performance profiling
3. Discussion

## 1. Load Testing Basic

### References

- Video reference:
  `Practical Performance Analysis by Simone Bordet`
  `Why you need performance tests for proper Kubernetes scaling By Dmitry Chuyko`
- Demo load test JMeter scenario:
  `nor-load-testing-plan.jmx`
- Azure Load Testing uses JMeter scenario:
  `What is Azure Load Testing? | Microsoft Learn`

### Frameworks and Tools

- Apache JMeter: `Apache JMeter - Apache JMeter™`
- Locust: `Locust - A modern load testing framework`

### Key Performance Metrics

| Metric | Category | Definition |
|---|---|---|
| Average Response Time | Response Time | Average time for the system to respond, indicating overall performance. |
| Peak Response Time | Response Time | Longest response time during the test, showing potential bottlenecks. |
| 95th/99th Percentile | Response Time | Time within which 95%/99% of requests are served, helping identify outliers. |
| Requests per Second (RPS) | Throughput | Number of requests handled per second, indicating processing capacity. |
| Transactions per Second (TPS) | Throughput | Number of transactions completed per second, important for interactive applications. |
| Error Rate | Error Rate | Percentage of failed requests, indicating stability and reliability under load. |
| Types of Errors | Error Rate | Breakdown of errors (e.g. `4xx`, `5xx` HTTP errors) for targeted troubleshooting. |
| Network Latency | Latency | Measures delays caused by network factors. |
| Server Processing Time | Latency | Reflects server delays excluding network latency, highlighting server-side optimization needs. |
| CPU Utilization | CPU and Memory Usage | Percentage of CPU resources used, showing CPU load. |
| Memory Usage | CPU and Memory Usage | Amount of memory used, highlighting potential memory-related bottlenecks. |
| Memory Swap | CPU and Memory Usage | Indicates memory overflow to disk, which can degrade performance. |
| Network Bandwidth Utilization | Network I/O | Amount of network capacity used, important for network resource planning. |
| Packet Loss | Network I/O | Percentage of data packets lost during transmission, indicating network quality issues. |
| Network Jitter | Network I/O | Variability in network latency, relevant for real-time applications (e.g. gaming, streaming). |
| Query Response Time | Database Performance | Time taken for a database query to execute, identifying potential slow queries. |
| Auto-scaling Events | Resource Utilization | Number of scaling activities, reflecting adaptability to changing loads. |
| Concurrent Users | Session Metrics | Number of users active at a given time, used to assess capacity limits. |
| Cache Hit Ratio | Cache Performance | Proportion of cache hits versus misses, indicating cache optimization level. |
| Cache Latency | Cache Performance | Time taken to retrieve data from cache, important for applications relying on fast access. |
| Time to First Byte (TTFB) | User Experience Metrics | Time to receive the first byte of response, indicating server responsiveness. |
| Page Load Time | User Experience Metrics | Total time to fully load a web page, affecting user satisfaction. |
| DOM Interactive Time | User Experience Metrics | Time for a page to become interactive, impacting perceived performance. |
| Cost per Request | Cost Metrics | Estimated cost associated with processing each request under load. |
| Resource Utilization Cost | Cost Metrics | Cost of resources during load, essential for budgeting and cost optimization in cloud setups. |

### Different Load Test Scenarios

| Scenario | Purpose | Scenario Description | Goal |
|---|---|---|---|
| Baseline Testing | Establish a performance baseline | Run with standard load (e.g. `100` users) | Set benchmarks for comparison with other scenarios. |
| Peak Load Testing | Test performance under expected high traffic | Simulate the highest expected user load (e.g. during an event) | Ensure stability and performance at peak traffic. |
| Spike Testing | Test resilience to sudden, extreme increases in traffic | Apply a sudden, high load spike, then return to normal | Observe if the system can handle and recover from spikes without issues. |
| Stress Testing | Find system breaking point | Gradually increase load beyond peak levels until failure | Determine max capacity and observe failure mode. |
| Endurance (Soak) Testing | Check stability over extended periods | Run consistent load for long duration (e.g. `24-72` hours) | Identify memory leaks and long-term degradation. |
| Scalability Testing | Assess system’s scalability | Gradually increase load while observing auto-scaling and resource allocation | Ensure efficient scaling under increasing load. |
| Capacity Testing | Define max user load | Increase user load until performance thresholds are hit | Determine the maximum number of users the system can handle within acceptable metrics. |
| Concurrency Testing | Evaluate handling of simultaneous user actions | Simulate multiple concurrent actions (e.g. logins, checkouts) | Identify bottlenecks and data consistency issues with simultaneous actions. |
| Geographically Distributed Load Testing | Test latency and load balancing across regions | Generate load from multiple geographic locations | Assess response times, CDN performance, and latency across regions. |
| Failover Testing | Verify failover capabilities | Simulate component failures (e.g. server or database outage) | Ensure traffic reroutes properly and the system stays operational. |
| Queue Testing | Check handling of queued tasks under load | Generate load to fill up application queues (e.g. message or connection queues) | Ensure queued tasks process timely and prevent backlogs. |
| Multi-Tenancy Testing | Test performance with multiple tenants | Simulate multiple tenants with different workloads (for multi-tenant SaaS apps) | Ensure fair resource allocation and isolation between tenants. |
| Configuration Testing | Find optimal configuration setup | Run tests with different configurations (e.g. cache sizes, network/database settings) | Identify configurations that optimize performance under load. |

## 2. Nexis K8s Performance Profiling

### Load-Test Scenarios

Note:
- `1m = 0.001` of a vCPU core
- `1 Mi = 1` megabyte
- All tests were run `3` times to get average results

### IAM & Auth, EMS API Instance

Other apps usually call IAM and Auth APIs, hence the number of concurrent requests should be multiplied by the number of apps (about `x5`).

- Baseline: `100` simultaneous threads (`~100` users) over `30` seconds
- Peakload: `250` simultaneous threads (`~250` users) over `30` seconds
- Spike: `500` simultaneous threads (`~500` users) over `5` seconds
- Stress: `1000` simultaneous threads (`~1000` users) over `30` seconds

### Other App Instances

- Baseline: `20` simultaneous threads (`~20` users) over `30` seconds
- Peakload: `50` simultaneous threads (`~50` users) over `30` seconds
- Spike: `50` simultaneous threads (`~50` users) over `5` seconds
- Stress: `200` simultaneous threads (`~200` users) over `30` seconds

### Test Setup 1

Use JMeter against `kubectl port-forward` from an individual pod to `localhost` to see how well the pod performs under load. Use `kubectl top pod` to observe CPU and memory metrics.

| App name | API(s) per thread | Idle cpu \| mem | Baseline cpu \| mem | Peakload cpu \| mem | Spike cpu \| mem |
|---|---|---|---|---|---|
| OR API | 8 API req(s) per thread | 1m \| 278Mi | 12m \| 355Mi | 21m \| 425Mi | 74m \| 440Mi |
| IAM API | 3 API req(s) per thread | 1m \| 270Mi | 2m \| 236Mi | 27m \| 270Mi | 150m \| 433Mi |

### Test Setup 2

Use JMeter against the public APIM URL of each individual app instance to see how well the pod performs under load. Use `kubectl top pod` to observe CPU and memory metrics.

The replica count of all app instances was set to `1` at the time of testing, so the observed CPU and memory metrics are effectively for an individual pod.

| App name | API(s) per thread | Idle cpu \| mem | Baseline cpu \| mem | Peakload cpu \| mem | Spike cpu \| mem | Stress cpu \| mem |
|---|---|---|---|---|---|---|
| OR API | 8 API req(s) per thread | 1m \| 278Mi | 41m \| 412Mi | 108m \| 577Mi | 100m \| 580Mi | 300m \| 546Mi |
| IAM API | 3 API req(s) per thread | 1m \| 270Mi | 35m \| 256Mi | 57m \| 421Mi | 252m \| 493Mi | 177m \| 520Mi |
| Auth API | *same scenario with IAM API* | 1m \| 242Mi | 31m \| 334Mi | 52m \| 336Mi | 136m \| 332Mi | 134m \| 287Mi |
| EMS API | `/api/v1/notifications` | 1m \| 300Mi | 12m \| 368Mi | 24m \| 375Mi | 34m \| 388Mi | 26m \| 462Mi |
| Portal Page | Customer Portal | 1m \| 5Mi | 1m \| 18Mi | 2m \| 18Mi | 4m \| 18Mi | 4m \| 18Mi |
| Report App | Online Report | 1m \| 24Mi | 1m \| 24Mi | 2m \| 25Mi |  |  |

### Charts

- CPU consumption over 4 load-test scenarios
- Memory consumption over 4 load-test scenarios
- Base memory per app instance

## 3. Discussion

These load-test results can be used as empirical references to set pod resource limits for each app instance.

- Request CPU and memory can be referenced from baseline load test results.
- Limit CPU and memory can be referenced from spike and stress load test results.
- Reference: `https://www.youtube.com/watch?v=Y8lmJvy8hJg&list=LL&`

### Notes

- Memory is an incompressible resource. A pod exceeding its memory limit will get terminated.
- CPU is a compressible resource. A pod exceeding its CPU limit gets throttled.

### Observations

- .NET runtime pods that experienced Peak, Spike, or Stress load do not release allocated memory afterward.
- Example: `or-api` and `iam-api` still consume around `~400Mi` of memory after the high load has finished.
- Possible hypothesis: .NET GC behavior inside the pod may not release memory back to the container as expected.
