def build_ai_prompt(company_name: str, website_url: str, email: str, website_data: dict[str, str]) -> str:
    auth_context = "You are a senior digital strategy consultant writing a consulting-grade audit report for a business owner."
    content = [
        auth_context,
        "",
        f"Company name: {company_name}",
        f"Website URL: {website_url}",
        f"Contact email: {email}",
        "",
        "Website scraping results:",
        f"Title: {website_data.get('website_title', '')}",
        f"Meta description: {website_data.get('website_description', '')}",
        f"Headings: {website_data.get('website_headings', '')}",
        f"Visible text excerpt: {website_data.get('website_text', '')[:1200]}",
        "",
        "Create a structured audit report with the following keys:",
        "executive_summary, business_model, digital_maturity, ux_observations, seo_observations, growth_recommendations, ai_opportunities, conclusion.",
        "",
        "Each key should contain 2-4 concise, professional paragraphs. Use a business-aware tone, avoid generic marketing language, and do not mention that you are an AI.",
        "Return the response as a valid JSON object only.",
    ]
    return "\n".join(content)
