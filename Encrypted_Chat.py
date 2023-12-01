import base64
import secrets
import json
import colorama
 
colorama.init(autoreset=True)

class Colors:
    RESET = '\033[0m'
    
    @staticmethod
    def rgb_color(r, g, b):
        # 使用 8 位颜色
        return f'\033[38;2;{r};{g};{b}m'
    
    @staticmethod
    def rgb_background_color(r, g, b):
        # 使用 8 位背景颜色
        return f'\033[48;2;{r};{g};{b}m'

def colored_text(text, color, background_color=None):
    color_code = Colors.rgb_color(*color)
    background_color_code = ""
    
    if background_color:
        background_color_code = Colors.rgb_background_color(*background_color)
    
    return f"{color_code}{background_color_code}{text}{Colors.RESET}"


def encrypt(text, key):
    # 实现加密算法，这里使用base64编码
    encrypted_text = base64.b64encode(text.encode()).decode()
    return encrypted_text

def decrypt(encrypted_text, key):
    # 实现解密算法，这里使用base64解码
    try:
        # 验证密钥是否正确
        if key != get_key_for_encrypted_text(encrypted_text):
            raise ValueError("\033[31m解密失败：密钥错误\033[0m")
        
        decrypted_text = base64.b64decode(encrypted_text).decode()
        return decrypted_text
    except Exception as e:
        raise ValueError("\033[31m解密失败：密钥错误或损坏\033[0m")

def get_key_for_encrypted_text(encrypted_text):
    # 获取加密时使用的密钥
    return records.get(encrypted_text)

def save_records_to_file(records, filename='records.json'):
    # 将记录保存到records.json文件
    with open(filename, 'w') as file:
        json.dump(records, file, indent=2)

def load_records_from_file(filename='records.json'):
    # 从records.json文件加载记录
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def generate_secure_key():
    # 生成安全性较强的密钥
    return secrets.token_hex(16)  # 16字节的随机十六进制数

def save_password_to_file(password, filename='password.json'):
    # 将密码保存到password.json文件
    with open(filename, 'w') as file:
        file.write(password)

def change_management_password():
    # 修改管理密码
    global management_password
    new_password = input("请输入新的管理密码：")
    management_password = new_password
    save_password_to_file(management_password)
    print("\033[36m管理密码已修改成功\033[0m")

def load_password_from_file(filename='password.json'):
    # 从password.json文件加载管理密码
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "default_password"  # 默认密码，可以根据需要修改

def main():
    global records, management_password
    records = load_records_from_file()  # 从文件加载记录
    management_password = "123456"  # 初始密码设置为123456
    save_password_to_file(management_password)
    management_password = load_password_from_file()  # 从文件加载管理密码

    separator = '-' * 118  # 分隔符
    print(separator)
    print('#'*47, colored_text("欢迎使用Encrypted Chat",(255,182,193)), '#'*47)
 
    while True:
        print(separator)
        choice = input("请选择操作：\n\n \033[30;47m 1 \033[0m 加密\n\n \033[30;47m 2 \033[0m 解密\n\n \033[30;47m 3 \033[0m 显示密钥（管理员）\n\n\
 \033[30;47m 4 \033[0m 清除所有记录\n\n \033[30;47m 5 \033[0m 修改管理密码\n\n>>")

        if choice == '1':
            # 加密
            plaintext = input("请输入需要加密的文本：")
            key_choice = input("\n请选择密钥的设置方式：\n1. 手动输入\n2. 自动生成\n>>")

            if key_choice == '1':
                key = input("请输入密钥：")
            elif key_choice == '2':
                key = generate_secure_key()
                print(f"生成的安全性较强的密钥：", colored_text(key, (210, 148, 122)), sep='')
            else:
                print("\033[31m无效的选择，请输入1或2\033[0m")
                continue

            encrypted_text = encrypt(plaintext, key)
            records[encrypted_text] = key  # 记录密钥
            save_records_to_file(records)  # 保存记录到文件
            print(f"加密后的文本：", colored_text(encrypted_text, (156, 220, 254)), sep='')

        elif choice == '2':
            # 解密
            encrypted_text = input("请输入需要解密的暗文：")
            key = input("请输入密钥：")

            try:
                decrypted_text = decrypt(encrypted_text, key)
                print(f"解密后的文本：\033[32m{decrypted_text}\033[0m")
            except ValueError as e:
                print(e)

        elif choice == '3':
            # 输入管理密码，显示对应暗文的密钥
            password_input = input("请输入管理密码：")
            if password_input == management_password:
                encrypted_text_to_show = input("请输入需要显示密钥的暗文：")
                key = get_key_for_encrypted_text(encrypted_text_to_show)
                if key is not None:
                    print(f"暗文", colored_text(encrypted_text_to_show, (156, 220, 254)), "\n对应的密钥是", colored_text(key, (210, 148, 122)))
                else:
                    print("\033[31m错误：找不到对应的记录\033[0m")
            else:
                print("\033[31m错误：管理密码错误\033[0m")

        elif choice == '4':
            # 清除所有记录
            password_input = input("请输入管理密码：")
            if password_input == management_password:
                confirm = input("\033[31m您确定要清除所有记录吗？这将无法恢复！\033[0m\n\033[33m输入 yes 确认：\033[0m\n>>")
                if confirm.lower() == 'yes':
                    records = {}  # 清空记录
                    save_records_to_file(records)  # 保存清空后的记录到文件
                    print("\033[36m所有记录已清除\033[0m")
                else:
                    print("\033[36m操作已取消\033[0m")
            else:
                print("\033[31m错误：管理密码错误\033[0m")

        elif choice == '5':
            # 修改管理密码
            password_input = input("请输入当前管理密码：")
            if password_input == management_password:
                change_management_password()
            else:
                print("\033[31m错误：管理密码错误\033[0m")

        else:
            print("\033[31m无效的选择，请输入1、2、3、4或5进行操作选择\033[0m")

if __name__ == "__main__":
    main()
