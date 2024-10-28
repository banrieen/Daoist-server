use prometheus::{Gauge, Histogram, Registry};
use tokio::task;

#[derive(Copy, Clone)]
struct MyMetric {
    name: String,
    value: u32,
}

async fn worker(id: u32) -> MyMetric {
    // Do some work here...
    let value = 12 ;/* calculate a value */
    let metric = MyMetric { name: format!("worker_{}", id), value };
    tokio::task::yield_now().await;
    metric
}

#[tokio::main]
async fn main() {
    let registry = Registry::new();
    let worker_metric = Gauge::new("worker_metric", "Worker metric").unwrap();
    let work_time_histogram = Histogram::new("work_time_histogram", "Work time histogram").unwrap();

    for i in 0..5 {
        let handle = task::spawn(worker(i));
        let metric = handle.await.unwrap();
        worker_metric.set(metric.value as f64);
        work_time_histogram.observe(metric.value as f64);
    }

    // Export metrics
    registry.gather().await;
}
