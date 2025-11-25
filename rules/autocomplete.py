from typing import List, Set
from .base import WCAGRule, Issue


class InputPurposeRule(WCAGRule):
    name = "Identify Input Purpose"
    criterion = "1.3.5"
    level = "AA"

    PERSONAL_DATA_NAMES: Set[str] = {
        'name', 'fname', 'firstname', 'first-name', 'first_name',
        'lname', 'lastname', 'last-name', 'last_name',
        'email', 'e-mail', 'mail',
        'phone', 'tel', 'telephone', 'mobile',
        'address', 'street', 'city', 'country', 'postal', 'zip', 'zipcode',
        'cc-number', 'card-number', 'cardnumber',
        'cc-exp', 'expiry', 'exp-date',
        'cc-csc', 'cvv', 'cvc', 'security-code',
        'username', 'login',
        'password', 'pass', 'pwd',
        'organization', 'company'
    }

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие autocomplete для полей персональных данных
        """
        issues = []
        soup = self._parse(html)

        for input_elem in soup.find_all('input'):
            input_type = input_elem.get('type', 'text').lower()

            if input_type not in ['text', 'email', 'tel', 'url', 'password']:
                continue

            name = input_elem.get('name', '').lower()
            input_id = input_elem.get('id', '').lower()

            is_personal = any(
                personal_field in name or personal_field in input_id
                for personal_field in self.PERSONAL_DATA_NAMES
            )

            if is_personal and not input_elem.has_attr('autocomplete'):
                field_identifier = name or input_id or 'без имени'
                issues.append(self._issue(
                    input_elem,
                    f'Поле персональных данных "{field_identifier}" не имеет атрибута autocomplete',
                    'Добавьте атрибут autocomplete с соответствующим значением (например, autocomplete="email")',
                    html
                ))

        return issues
