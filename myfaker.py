from faker import Faker
import random

# 创建 Faker 实例并设置区域为台湾
fake = Faker('zh_TW')

def generate_credit_card_number():
    # 随机选择 VISA、MasterCard 或 JCB
    card_type = random.choice(['visa16', 'mastercard', 'jcb15'])
    return fake.credit_card_number(card_type=card_type)

def generate_credit_card_expiration_date():
    # 生成有效期限，通常为 2 位数月份和 2 位数年份
    expiration_date = fake.date_between(start_date='+1d', end_date='+10y')
    return expiration_date.strftime('%m/%y')  # 使用 strftime 格式化日期
    
def generate_credit_card_cvv():
    # 生成 3 位数的 CVV 安全码
    return fake.credit_card_security_code()

def generate_credit_card_holder_name():
    # 生成持卡人姓名
    return fake.name()

def generate_phone_number():
    fake = Faker('zh_TW')
    phone_number = '09' + str(fake.random_number(digits=8))
    return phone_number

def generate_email():
    # 生成邮箱
    return fake.email()

def generate_billing_address():
    # 生成帐单地址
    return fake.address()

# 示例用法
credit_card_number = generate_credit_card_number()
expiration_date = generate_credit_card_expiration_date()
cvv = generate_credit_card_cvv()
holder_name = generate_credit_card_holder_name()
phone_number = generate_phone_number()
email = generate_email()
billing_address = generate_billing_address()

print(f"信用卡号码: {credit_card_number}")
print(f"有效期限: {expiration_date}")
print(f"CVV 安全码: {cvv}")
print(f"持卡人姓名: {holder_name}")
print(f"手机号码: {phone_number}")
print(f"电子邮箱: {email}")
print(f"帐单地址: {billing_address}")
