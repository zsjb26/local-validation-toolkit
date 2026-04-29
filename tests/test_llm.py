from lvt.llm import summarize_validation_results


sample = """
[PASS] Config validation succeeded
scan_name=home_network_quick_check
target_cidr=192.168.50.0/24
log_level=INFO
max_hosts=64
enable_llm_summary=false
"""

summary = summarize_validation_results(sample)

print("\n[LLM SUMMARY]")
print(summary)