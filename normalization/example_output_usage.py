"""
Example usage of output generation and comparison metrics.

This script demonstrates how to use the output service to generate
structured JSON output with comparison metrics.
"""

from datetime import datetime
import uuid

from data_models import (
    NormalizedLoanData,
    LoanType,
    BankInfo,
    FeeItem,
    PaymentScheduleEntry,
    TableData,
    CoSignerDetails
)
from output_service import OutputService


def create_sample_loan_data() -> NormalizedLoanData:
    """Create sample loan data for demonstration."""
    
    # Create bank info
    bank_info = BankInfo(
        bank_name="State Bank of India",
        branch_name="Mumbai Central",
        bank_code="SBI001"
    )
    
    # Create fees
    fees = [
        FeeItem(fee_type="processing", amount=5000.0, currency="INR"),
        FeeItem(fee_type="administrative", amount=1000.0, currency="INR"),
        FeeItem(fee_type="documentation", amount=500.0, currency="INR")
    ]
    
    # Create payment schedule
    payment_schedule = [
        PaymentScheduleEntry(
            payment_number=1,
            payment_date="2024-01-15",
            total_amount=8500.0,
            principal_component=5000.0,
            interest_component=3500.0,
            outstanding_balance=495000.0
        ),
        PaymentScheduleEntry(
            payment_number=2,
            payment_date="2024-02-15",
            total_amount=8500.0,
            principal_component=5100.0,
            interest_component=3400.0,
            outstanding_balance=489900.0
        )
    ]
    
    # Create table data
    fee_table = TableData(
        table_id="table_001",
        headers=["Fee Type", "Amount", "Conditions"],
        rows=[
            ["Processing Fee", "5000", "One-time"],
            ["Administrative Fee", "1000", "Annual"],
            ["Documentation Fee", "500", "One-time"]
        ],
        table_type="fee_structure"
    )
    
    # Create co-signer
    co_signer = CoSignerDetails(
        name="John Doe",
        relationship="Father",
        contact="+91-9876543210"
    )
    
    # Create normalized loan data
    loan_data = NormalizedLoanData(
        loan_id=str(uuid.uuid4()),
        document_id=str(uuid.uuid4()),
        loan_type=LoanType.EDUCATION,
        bank_info=bank_info,
        principal_amount=500000.0,
        currency="INR",
        interest_rate=8.5,
        tenure_months=60,
        moratorium_period_months=6,
        fees=fees,
        processing_fee=5000.0,
        late_payment_penalty="2% per month on overdue amount",
        prepayment_penalty="No penalty after 12 months",
        repayment_mode="EMI",
        payment_schedule=payment_schedule,
        co_signer=co_signer,
        collateral_details="None",
        disbursement_terms="Direct to institution",
        tables=[fee_table],
        extraction_confidence=0.95,
        extraction_timestamp=datetime.now(),
        raw_extracted_fields={
            "original_principal": "Rs. 5,00,000",
            "original_rate": "8.5% p.a."
        }
    )
    
    return loan_data


def main():
    """Main demonstration function."""
    
    print("=" * 60)
    print("Loan Document Output Generation Demo")
    print("=" * 60)
    print()
    
    # Create output service
    output_service = OutputService(output_directory="./output")
    
    # Create sample loan data
    print("Creating sample loan data...")
    loan_data = create_sample_loan_data()
    print(f"✓ Created loan data for {loan_data.loan_type.value} loan")
    print(f"  Principal: {loan_data.currency} {loan_data.principal_amount:,.2f}")
    print(f"  Interest Rate: {loan_data.interest_rate}%")
    print(f"  Tenure: {loan_data.tenure_months} months")
    print()
    
    # Generate complete output
    print("Generating complete output with metrics...")
    output_doc = output_service.generate_complete_output(
        loan_data,
        source_document_path="/documents/education_loan_001.pdf",
        save_to_file=True
    )
    print("✓ Output generated successfully")
    print()
    
    # Display comparison metrics
    if "comparison_metrics" in output_doc:
        metrics = output_doc["comparison_metrics"]
        print("Comparison Metrics:")
        print(f"  Total Cost Estimate: {metrics['total_cost_estimate']:,.2f}")
        print(f"  Effective Interest Rate: {metrics['effective_interest_rate']}%")
        print(f"  Flexibility Score: {metrics['flexibility_score']}/10.0")
        print(f"  Monthly EMI: {metrics['monthly_emi']:,.2f}")
        print(f"  Total Interest Payable: {metrics['total_interest_payable']:,.2f}")
        print()
    
    # Get JSON string
    print("Generating JSON string...")
    json_string = output_service.get_json_string(
        loan_data,
        include_metrics=True,
        pretty=True
    )
    print("✓ JSON string generated")
    print()
    print("Sample JSON Output (first 500 characters):")
    print("-" * 60)
    print(json_string[:500] + "...")
    print("-" * 60)
    print()
    
    # Create multiple loans for comparison
    print("Creating multiple loans for comparison...")
    loan_data_2 = create_sample_loan_data()
    loan_data_2.loan_id = str(uuid.uuid4())
    loan_data_2.principal_amount = 600000.0
    loan_data_2.interest_rate = 7.5
    loan_data_2.moratorium_period_months = 12
    
    loan_data_3 = create_sample_loan_data()
    loan_data_3.loan_id = str(uuid.uuid4())
    loan_data_3.principal_amount = 450000.0
    loan_data_3.interest_rate = 9.0
    loan_data_3.moratorium_period_months = 3
    
    # Generate comparison
    comparison_result = output_service.generate_comparison_output(
        [loan_data, loan_data_2, loan_data_3],
        save_to_file=False
    )
    
    print(f"✓ Compared {len(comparison_result.loans)} loans")
    print(f"  Best by Cost: {comparison_result.best_by_cost}")
    print(f"  Best by Flexibility: {comparison_result.best_by_flexibility}")
    print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
