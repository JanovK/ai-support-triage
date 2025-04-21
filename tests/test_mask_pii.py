from src.mask_pii import mask_text

def test_email_masking():
    input_text = "Please contact john.doe@example.com for more info."
    masked = mask_text(input_text)
    assert "[EMAIL_REDACTED]" in masked

def test_phone_masking():
    input_text = "Call me at +1 (514) 123-4567"
    masked = mask_text(input_text)
    assert "[PHONE_REDACTED]" in masked

def test_person_entity():
    input_text = "Barack Obama was the president."
    masked = mask_text(input_text)
    assert "[PERSON_REDACTED]" in masked

def test_credit_card_masking():
    input_text = "My card number is 4111 1111 1111 1111"
    masked = mask_text(input_text)
    assert "[CREDIT_CARD_REDACTED]" in masked
