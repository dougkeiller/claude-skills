# Spend audit from Hermes logs

Use when asked what a model setup costs, or when a provider reports a spending cap or limit.

## Procedure

1. Read the provider's error text first. A 403 or 429 usually names the cap and its reset time. Quote that text. Do not infer the cause from which model failed.
2. Pull per-call token counts from `~/.hermes/logs/agent.log`. Lines containing `API call #` carry `model=`, `provider=`, `in=`, and `out=`. Some lines also carry `cache=<read>/<total>`. Filter on the date prefix at the start of each line, then group by date, provider and model.
3. Treat MoA as a special case. MoA aggregator calls appear as `provider=moa` with the preset name as the model. Adviser calls were not confirmed as separate log lines, so do not claim a per-adviser split until you have checked the log for it.
4. Get prices from a live source, not from memory. OpenRouter's public model list (`curl -s https://openrouter.ai/api/v1/models`) gives `pricing.prompt`, `pricing.completion` and `pricing.input_cache_read` as per-token strings. Multiply by 1,000,000 for a per-million figure. Native providers publish their own pricing pages; use those. Record the as-of date beside every price.
5. Estimate each group as: (input − cached) × input price + cached × cache-read price + output × output price. The log does not show cache-write charges, so say they are left out.
6. Report the figure as an estimate. Give the method, the price date and the source for each provider. Where a provider has no per-token price (a subscription or OAuth login), report tokens only and say no dollar figure is available.

## Pitfalls

- Counting only the aggregator understates spend whenever advisers run. Name every provider in the setup and say which of its calls the log does not show.
- If the provider's own usage page is reachable, compare the estimate with it. Where the two differ, present the usage page as the bill and the log estimate as a rough check.
- Long sessions dominate cost. Input tokens are resent on every tool step, so a few long chats can outweigh many short ones; report the largest sessions by input tokens as well as the totals.
