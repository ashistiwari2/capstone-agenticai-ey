import re
from importlib.machinery import SourceFileLoader
from utils.pii_filter import redact_pii

generator = SourceFileLoader("generator", "src/04_generate_grounded.py").load_module()

APPROVAL_TERMS = {"approve", "approval", "sanction", "reject", "waive", "modify loan", "disburse"}

def calculate_emi(principal: float, annual_rate: float, months: int):
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    total = emi * months
    return {
        "emi": round(emi, 2),
        "total_payment": round(total, 2),
        "total_interest": round(total - principal, 2),
    }

def extract_emi_numbers(text):
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]
    if len(nums) >= 3:
        return nums[0], nums[1], int(nums[2])
    return None

def needs_human_approval(text):
    lower = text.lower()
    return any(term in lower for term in APPROVAL_TERMS)

def route(user_input):
    safe_input = redact_pii(user_input)
    if needs_human_approval(safe_input):
        print("Human approval required before this action can proceed.")
        decision = input("Authorised reviewer decision (approve/deny): ").strip().lower()
        if decision == "approve":
            return "Reviewer approved the workflow step. Note: this demo does not sanction or modify any real loan."
        return "Request denied or not approved by reviewer. No loan action was taken."

    if "emi" in safe_input.lower() or "monthly instal" in safe_input.lower():
        parsed = extract_emi_numbers(safe_input)
        if not parsed:
            return "Please provide principal, annual interest rate, and tenure in months. Example: EMI for 1200000 at 9.5 for 60 months."
        principal, annual_rate, months = parsed
        result = calculate_emi(principal, annual_rate, months)
        return (
            f"Estimated EMI: {result['emi']}\n"
            f"Total payment: {result['total_payment']}\n"
            f"Total interest: {result['total_interest']}\n"
            "This is an estimate. Final repayment schedule depends on bank sanction terms."
        )

    response, _ = generator.answer(safe_input)
    return response

def main():
    print("Banking Loan Assistant. Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        print("\nAssistant:")
        print(route(user_input))

if __name__ == "__main__":
    main()
