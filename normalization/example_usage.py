"""
Example usage of the normalization module.

This script demonstrates how to use the normalization service to validate
and normalize extracted loan data.
"""

from datetime import date
from normalization import (
    NormalizationService,
    normalize_loan_data,
    quick_normalize,
    LoanType
)


def example_basic_normalization():
    """Example of basic normalization workflow."""
    print("=" * 60)
    print("Example 1: Basic Normalization")
    print("=" * 60)
    
    # Sample extracted data (as it would come from extraction module)
    extracted_data = {
        'loan_type': 'education',
        'bank_name': 'State Bank of India',
        'branch_name': 'Mumbai Central',
        'principal_amount': '₹5,00,000',
        'interest_rate': '8.5%',
        'tenure': '5 years',
        'moratorium_period': '6 months',
        'processing_fee': '₹5,000',
        'late_payment_penalty': '2% per month on overdue amount',
        'prepayment_penalty': 'Nil after 12 months',
        'repayment_mode': 'EMI',
        'confidence': 0.95
    }
    
    document_id = 'doc_12345'
    
    # Normalize the data
    result = normalize_loan_data(extracted_data, document_id)
    
    # Check result
    if result.is_valid:
        print("✓ Normalization successful!")
        print(f"\nLoan ID: {result.validated_data.loan_id}")
        print(f"Principal: {result.validated_data.currency} {result.validated_data.principal_amount:,.2f}")
        print(f"Interest Rate: {result.validated_data.interest_rate}%")
        print(f"Tenure: {result.validated_data.tenure_months} months")
        
        if result.warnings:
            print(f"\nWarnings ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  - {warning}")
    else:
        print("✗ Normalization failed!")
        print(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  - {error.field}: {error.message}")
    
    print()


def example_with_payment_schedule():
    """Example with payment schedule data."""
    print("=" * 60)
    print("Example 2: Normalization with Payment Schedule")
    print("=" * 60)
    
    extracted_data = {
        'loan_type': 'personal',
        'bank_name': 'HDFC Bank',
        'principal': 200000,
        'interest_rate': 12.5,
        'tenure': '24 months',
        'repayment_mode': 'EMI',
        'payment_schedule': [
            {
                'payment_number': 1,
                'payment_date': '2024-02-01',
                'total_amount': 9456.78,
                'principal': 7373.45,
                'interest': 2083.33,
                'balance': 192626.55
            },
            {
                'payment_number': 2,
                'payment_date': '2024-03-01',
                'total_amount': 9456.78,
                'principal': 7450.12,
                'interest': 2006.66,
                'balance': 185176.43
            }
        ],
        'confidence': 0.92
    }
    
    document_id = 'doc_67890'
    
    result = normalize_loan_data(extracted_data, document_id)
    
    if result.is_valid:
        print("✓ Normalization successful!")
        loan = result.validated_data
        print(f"\nLoan Details:")
        print(f"  Type: {loan.loan_type.value}")
        print(f"  Bank: {loan.bank_info.bank_name}")
        print(f"  Principal: {loan.currency} {loan.principal_amount:,.2f}")
        
        if loan.payment_schedule:
            print(f"\nPayment Schedule ({len(loan.payment_schedule)} entries):")
            for entry in loan.payment_schedule[:2]:  # Show first 2
                print(f"  Payment {entry.payment_number}: {entry.payment_date}")
                print(f"    Total: {entry.total_amount:,.2f}")
                print(f"    Principal: {entry.principal_component:,.2f}")
                print(f"    Interest: {entry.interest_component:,.2f}")
    else:
        print("✗ Normalization failed!")
        for error in result.errors:
            print(f"  - {error.field}: {error.message}")
    
    print()


def example_with_fees():
    """Example with multiple fees."""
    print("=" * 60)
    print("Example 3: Normalization with Multiple Fees")
    print("=" * 60)
    
    extracted_data = {
        'loan_type': 'home',
        'bank_name': 'ICICI Bank',
        'branch': 'Delhi Branch',
        'principal_amount': 5000000,
        'interest_rate': 7.5,
        'tenure_months': 240,
        'fees': [
            {
                'type': 'Processing Fee',
                'amount': 25000,
                'currency': 'INR',
                'conditions': 'One-time at disbursement'
            },
            {
                'type': 'Legal Fee',
                'amount': 15000,
                'currency': 'INR'
            },
            {
                'type': 'Valuation Fee',
                'amount': 5000,
                'currency': 'INR'
            }
        ],
        'collateral': 'Residential property at Mumbai',
        'confidence': 0.88
    }
    
    document_id = 'doc_home_001'
    
    service = NormalizationService()
    result = service.normalize(extracted_data, document_id)
    
    if result.is_valid:
        print("✓ Normalization successful!")
        loan = result.validated_data
        
        print(f"\nLoan Details:")
        print(f"  Type: {loan.loan_type.value.title()} Loan")
        print(f"  Bank: {loan.bank_info.bank_name}")
        print(f"  Principal: {loan.currency} {loan.principal_amount:,.2f}")
        print(f"  Tenure: {loan.tenure_months // 12} years")
        
        if loan.fees:
            print(f"\nFees ({len(loan.fees)} items):")
            total_fees = 0
            for fee in loan.fees:
                print(f"  - {fee.fee_type}: {fee.currency} {fee.amount:,.2f}")
                total_fees += fee.amount
            print(f"  Total Fees: {loan.currency} {total_fees:,.2f}")
        
        if loan.collateral_details:
            print(f"\nCollateral: {loan.collateral_details}")
        
        # Get as JSON
        json_output = service.get_normalized_json(result)
        print(f"\nJSON output length: {len(json_output)} characters")
    else:
        print("✗ Normalization failed!")
    
    print()


def example_validation_errors():
    """Example showing validation errors."""
    print("=" * 60)
    print("Example 4: Validation Errors")
    print("=" * 60)
    
    # Invalid data (missing required fields, invalid values)
    extracted_data = {
        'loan_type': 'education',
        'bank_name': 'Test Bank',
        # Missing principal_amount (required)
        'interest_rate': 150,  # Invalid: too high
        'tenure': '-5 months',  # Invalid: negative
        'confidence': 1.5  # Invalid: > 1.0
    }
    
    document_id = 'doc_invalid'
    
    result = normalize_loan_data(extracted_data, document_id)
    
    print(f"Validation Status: {'✓ Valid' if result.is_valid else '✗ Invalid'}")
    
    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  Field: {error.field}")
            print(f"  Type: {error.error_type}")
            print(f"  Message: {error.message}")
            print()
    
    if result.warnings:
        print(f"Warnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    print()


def example_quick_normalize():
    """Example using quick_normalize convenience function."""
    print("=" * 60)
    print("Example 5: Quick Normalize")
    print("=" * 60)
    
    extracted_data = {
        'loan_type': 'vehicle',
        'bank_name': 'Axis Bank',
        'principal': 800000,
        'interest_rate': 9.5,
        'tenure': '60 months',
        'confidence': 0.91
    }
    
    document_id = 'doc_vehicle_001'
    
    # Quick normalize returns data directly or None
    loan_data = quick_normalize(extracted_data, document_id)
    
    if loan_data:
        print("✓ Quick normalization successful!")
        print(f"\nLoan ID: {loan_data.loan_id}")
        print(f"Type: {loan_data.loan_type.value.title()} Loan")
        print(f"Bank: {loan_data.bank_info.bank_name}")
        print(f"Amount: {loan_data.currency} {loan_data.principal_amount:,.2f}")
        print(f"Rate: {loan_data.interest_rate}%")
        print(f"Tenure: {loan_data.tenure_months} months")
    else:
        print("✗ Quick normalization failed!")
    
    print()


def example_batch_normalization():
    """Example of batch normalization."""
    print("=" * 60)
    print("Example 6: Batch Normalization")
    print("=" * 60)
    
    # Multiple loan documents
    extracted_data_list = [
        {
            'loan_type': 'education',
            'bank_name': 'SBI',
            'principal': 300000,
            'interest_rate': 8.0,
            'tenure': '48 months',
            'confidence': 0.94
        },
        {
            'loan_type': 'personal',
            'bank_name': 'HDFC',
            'principal': 150000,
            'interest_rate': 11.5,
            'tenure': '36 months',
            'confidence': 0.89
        },
        {
            'loan_type': 'home',
            'bank_name': 'ICICI',
            'principal': 4000000,
            'interest_rate': 7.25,
            'tenure': '300 months',
            'confidence': 0.92
        }
    ]
    
    document_ids = ['doc_001', 'doc_002', 'doc_003']
    
    service = NormalizationService()
    results = service.normalize_batch(extracted_data_list, document_ids)
    
    print(f"Processed {len(results)} documents\n")
    
    for i, result in enumerate(results, 1):
        status = "✓" if result.is_valid else "✗"
        print(f"{status} Document {i} ({document_ids[i-1]}): ", end="")
        
        if result.is_valid:
            loan = result.validated_data
            print(f"{loan.loan_type.value.title()} Loan - {loan.bank_info.bank_name}")
            print(f"   Amount: {loan.currency} {loan.principal_amount:,.2f}")
        else:
            print(f"Failed with {len(result.errors)} errors")
    
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("NORMALIZATION MODULE - EXAMPLE USAGE")
    print("=" * 60 + "\n")
    
    example_basic_normalization()
    example_with_payment_schedule()
    example_with_fees()
    example_validation_errors()
    example_quick_normalize()
    example_batch_normalization()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
