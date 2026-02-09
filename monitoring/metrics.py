"""
K.A.O.S. Monitoring & Observability Configuration
Prometheus metrics, logging, and health checks
"""

import time
from typing import Dict, Any
from datetime import datetime


class MetricsCollector:
    """Centralized metrics collection"""
    
    def __init__(self):
        """Initialize metrics"""
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_error": 0,
            "request_duration_sum": 0.0,
            "llm_queries": 0,
            "llm_latency_sum": 0.0,
            "fallback_activations": 0,
            "analysis_cache_hits": 0,
            "analysis_cache_misses": 0,
        }
        self.start_time = datetime.now()

    def record_request(
        self,
        duration: float,
        success: bool = True,
    ) -> None:
        """Record API request metrics"""
        self.metrics["requests_total"] += 1
        if success:
            self.metrics["requests_success"] += 1
        else:
            self.metrics["requests_error"] += 1
        self.metrics["request_duration_sum"] += duration

    def record_llm_query(self, latency: float) -> None:
        """Record LLM query metrics"""
        self.metrics["llm_queries"] += 1
        self.metrics["llm_latency_sum"] += latency

    def record_fallback(self) -> None:
        """Record fallback activation"""
        self.metrics["fallback_activations"] += 1

    def record_cache_hit(self) -> None:
        """Record cache hit"""
        self.metrics["analysis_cache_hits"] += 1

    def record_cache_miss(self) -> None:
        """Record cache miss"""
        self.metrics["analysis_cache_misses"] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot"""
        uptime = (
            datetime.now() - self.start_time
        ).total_seconds()
        
        avg_request_duration = (
            self.metrics["request_duration_sum"]
            / self.metrics["requests_total"]
            if self.metrics["requests_total"] > 0 else 0
        )
        
        avg_llm_latency = (
            self.metrics["llm_latency_sum"]
            / self.metrics["llm_queries"]
            if self.metrics["llm_queries"] > 0 else 0
        )
        
        cache_hit_rate = (
            self.metrics["analysis_cache_hits"]
            / (
                self.metrics["analysis_cache_hits"]
                + self.metrics["analysis_cache_misses"]
            )
            if (
                self.metrics["analysis_cache_hits"]
                + self.metrics["analysis_cache_misses"]
            ) > 0 else 0
        )
        
        return {
            "uptime_seconds": uptime,
            "requests": {
                "total": self.metrics["requests_total"],
                "success": self.metrics["requests_success"],
                "error": self.metrics["requests_error"],
                "error_rate": (
                    self.metrics["requests_error"]
                    / self.metrics["requests_total"]
                    if self.metrics["requests_total"] > 0 else 0
                ),
                "avg_duration_ms": avg_request_duration * 1000,
            },
            "llm": {
                "queries_total": self.metrics["llm_queries"],
                "avg_latency_ms": avg_llm_latency * 1000,
            },
            "fallback": {
                "activations": self.metrics[
                    "fallback_activations"
                ],
                "fallback_rate": (
                    self.metrics["fallback_activations"]
                    / self.metrics["requests_total"]
                    if self.metrics["requests_total"] > 0 else 0
                ),
            },
            "cache": {
                "hits": self.metrics["analysis_cache_hits"],
                "misses": self.metrics[
                    "analysis_cache_misses"
                ],
                "hit_rate": cache_hit_rate,
            },
        }

    def reset(self) -> None:
        """Reset metrics"""
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_error": 0,
            "request_duration_sum": 0.0,
            "llm_queries": 0,
            "llm_latency_sum": 0.0,
            "fallback_activations": 0,
            "analysis_cache_hits": 0,
            "analysis_cache_misses": 0,
        }


# Global metrics instance
_metrics_instance = None


def get_metrics_collector() -> MetricsCollector:
    """Get or create metrics collector singleton"""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = MetricsCollector()
    return _metrics_instance
