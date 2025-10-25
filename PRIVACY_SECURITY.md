# 🔒 Privacy & Security Guide

## Overview

The Student Loan Document Extractor Platform implements **comprehensive data masking and privacy protection** to safeguard sensitive user information.

## 🛡️ What We Protect

### Automatically Masked Information

All sensitive personal data is automatically masked before storage or display:

#### 1. **Personal Information**
- ✅ Full names (borrowers, co-signers)
- ✅ Physical addresses
- ✅ Date of birth
- ✅ Personal identifiers

#### 2. **Contact Information**
- ✅ Email addresses
- ✅ Phone numbers
- ✅ Mobile numbers
- ✅ Fax numbers

#### 3. **Financial Information**
- ✅ Account numbers
- ✅ Bank account details
- ✅ Loan account numbers
- ✅ Credit card numbers (if present)

#### 4. **Identification Numbers**
- ✅ Social Security Numbers (SSN)
- ✅ Driver's License numbers
- ✅ Passport numbers
- ✅ Tax ID numbers

#### 5. **Text Content**
- ✅ Emails in document text
- ✅ Phone numbers in document text
- ✅ SSN patterns in text
- ✅ Other PII in raw text

## 🎚️ Masking Levels

Choose the level of privacy protection that suits your needs:

### 1. **Minimal Masking**
*Best for: Personal use, when you need to see more details*

**What's shown:**
- First name visible, last name masked
- Last 4 digits of phone numbers
- First 2 characters of email
- City and state in addresses

**Example:**
- Name: `John ****`
- Email: `jo***@example.com`
- Phone: `***-***-1234`
- Address: `*** Los Angeles, CA`

### 2. **Standard Masking** (Recommended)
*Best for: Most users, balanced privacy and usability*

**What's shown:**
- First letter of first name
- Area code of phone numbers
- First character of email
- State/country only in addresses

**Example:**
- Name: `J*** ****`
- Email: `j***@***.com`
- Phone: `(555) ***-****`
- Address: `*** CA`

### 3. **Strict Masking**
*Best for: Maximum privacy, sharing with others*

**What's shown:**
- All names completely masked
- All contact info masked
- All addresses masked
- All account numbers masked

**Example:**
- Name: `*********`
- Email: `***@***.***`
- Phone: `***-***-****`
- Address: `[Address Masked]`

## 🔐 How It Works

### Processing Pipeline

```
Document Upload
    ↓
OCR Extraction
    ↓
AI Analysis
    ↓
Data Extraction
    ↓
🔒 DATA MASKING 🔒  ← Automatic privacy protection
    ↓
Storage
    ↓
Display/Download
```

### Masking Process

1. **Detection**: System identifies sensitive data patterns
2. **Classification**: Categorizes data by sensitivity level
3. **Masking**: Applies appropriate masking based on level
4. **Verification**: Ensures all sensitive data is protected
5. **Metadata**: Records what was masked for transparency

## 📊 What's NOT Masked

The following information remains visible for analysis:

✅ **Loan Terms:**
- Interest rates
- Loan amounts (principal)
- Tenure/duration
- EMI amounts
- Fees and charges

✅ **Bank Information:**
- Bank name
- Branch name (general)
- Product names
- Loan types

✅ **Document Information:**
- Document type
- Processing dates
- Confidence scores
- Extraction metadata

✅ **General Information:**
- Terms and conditions (general)
- Eligibility criteria (general)
- Office hours
- Website URLs (bank websites)

## 🎯 Using Privacy Features

### 1. Select Masking Level

```
1. Go to Upload Documents
2. Expand "🔒 Privacy & Data Protection"
3. Select your preferred masking level
4. Upload documents
```

### 2. View Masked Data

```
1. Open any processed document
2. See "🔒 Protected" status indicator
3. Check masked fields in expander
4. Review data with privacy protection
```

### 3. Download Protected Data

```
1. Click "Download JSON"
2. Masked data is included
3. Original sensitive info NOT included
4. Safe to share or store
```

## 🔍 Transparency

### Masking Metadata

Every masked document includes transparency information:

```json
{
  "_data_masking": {
    "masked": true,
    "mask_level": "standard",
    "masked_fields": [
      "borrower_name",
      "email",
      "phone_number",
      "address"
    ],
    "note": "Sensitive information has been masked for privacy"
  }
}
```

### What You Can See

- ✅ Which fields were masked
- ✅ What masking level was used
- ✅ When masking was applied
- ✅ How many fields were protected

## 🛡️ Security Best Practices

### For Users

1. **Choose Appropriate Level**
   - Use "Standard" for most cases
   - Use "Strict" when sharing data
   - Use "Minimal" only for personal use

2. **Verify Masking**
   - Check for 🔒 Protected indicator
   - Review masked fields list
   - Ensure sensitive data is hidden

3. **Safe Sharing**
   - Always download masked versions
   - Don't share original documents
   - Use strict masking for external sharing

4. **Data Retention**
   - Delete documents when no longer needed
   - Clear browser cache regularly
   - Don't store unmasked data

### For Administrators

1. **Default to Standard**
   - Set "standard" as default level
   - Educate users on options
   - Monitor masking effectiveness

2. **Audit Regularly**
   - Review masked data samples
   - Check for masking failures
   - Update patterns as needed

3. **Compliance**
   - Ensure GDPR compliance
   - Follow COPPA requirements
   - Maintain audit logs

## 📋 Compliance

### GDPR (General Data Protection Regulation)

✅ **Right to Privacy**: Data automatically masked
✅ **Data Minimization**: Only necessary data stored
✅ **Purpose Limitation**: Data used only for analysis
✅ **Storage Limitation**: Configurable retention
✅ **Integrity & Confidentiality**: Encryption + masking

### COPPA (Children's Online Privacy Protection Act)

✅ **Parental Consent**: Required for minors
✅ **Data Protection**: Enhanced masking for student data
✅ **Limited Collection**: Minimal data retention
✅ **Secure Storage**: Encrypted and masked

### CCPA (California Consumer Privacy Act)

✅ **Right to Know**: Transparency in masking
✅ **Right to Delete**: Data deletion available
✅ **Right to Opt-Out**: Masking level control
✅ **Non-Discrimination**: No penalty for privacy choices

## 🔧 Technical Details

### Masking Algorithms

**Name Masking:**
```python
"John Smith" → "J*** ****"  (standard)
"John Smith" → "John ****"  (minimal)
"John Smith" → "*********"  (strict)
```

**Email Masking:**
```python
"user@example.com" → "u***@***.com"  (standard)
"user@example.com" → "us***@example.com"  (minimal)
"user@example.com" → "***@***.***"  (strict)
```

**Phone Masking:**
```python
"555-123-4567" → "(555) ***-****"  (standard)
"555-123-4567" → "***-***-4567"  (minimal)
"555-123-4567" → "***-***-****"  (strict)
```

### Pattern Detection

The system uses regex patterns to detect:
- Email addresses: `[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}`
- Phone numbers: `\d{3}[-.]?\d{3}[-.]?\d{4}`
- SSN: `\d{3}-\d{2}-\d{4}`
- Account numbers: Various patterns

## 🚨 Important Notes

### What Masking Does

✅ **Protects** sensitive personal information
✅ **Enables** safe data sharing
✅ **Maintains** data utility for analysis
✅ **Provides** transparency in protection

### What Masking Doesn't Do

❌ **Not encryption** - Masked data is not encrypted
❌ **Not reversible** - Original data cannot be recovered
❌ **Not 100% foolproof** - Review data before sharing
❌ **Not a substitute** for secure storage

### Limitations

- Masking works on detected patterns
- Unusual formats may not be detected
- Context-based PII may be missed
- Always review before sharing externally

## 📞 Support

### Questions?

- Check masked fields in document viewer
- Review this guide for details
- Contact support for assistance

### Report Issues

If you find unmasked sensitive data:
1. Note the document and field
2. Report to security team
3. Don't share the data
4. Wait for fix confirmation

---

## 🎓 Summary

**Your privacy is our priority.** The platform automatically masks all sensitive personal information while preserving the data needed for loan analysis. Choose your preferred masking level, verify protection, and share data safely.

**Remember**: Always use "Strict" masking when sharing data externally!

🔒 **Protected by Design** | 🛡️ **Privacy First** | ✅ **GDPR Compliant**
