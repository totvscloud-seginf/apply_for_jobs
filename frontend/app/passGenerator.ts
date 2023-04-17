interface IPassGenOptions {
    is_special: boolean;
    is_number: boolean;
    is_uppercase: boolean;
    is_lowercase: boolean;
    length: number;
}

export const passwordGenerator = ({ is_special, is_number, is_uppercase, is_lowercase, length }: IPassGenOptions) : string => {
    if(length < 8) {
      throw new Error("Password length must be at least 8 characters.");
    }

    let characters = '';
    characters = setUpperCase(is_uppercase);
    characters += setLowerCase(is_lowercase);
    characters += setSpecial(is_special);
    characters += setNumber(is_number);

    return passwordCharacters(characters, length) ?? '';

    
}

const setUpperCase = (is_uppercase: boolean) => {
    if (is_uppercase) {
        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    }
    return '';
}

const setLowerCase = (is_lowercase: boolean) => {
    if (is_lowercase) {
        return 'abcdefghijklmnopqrstuvwxyz';
    }
    return '';
}

const setNumber = (is_number: boolean) => {
    if (is_number) {
        return '0123456789';
    }
    return '';
}

const setSpecial = (is_special: boolean) => {
    if (is_special) {
        return '!@#$%^&*()_+~`|}{[]\:;?><,./-=';
    }
    return '';
}

const getRandomInteger = (min: number, max: number) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const passwordCharacters = (characters: string, passwordLength: number) => {
    let password = '';
    if (characters.length) {
        for (let i = 0; i < passwordLength; i++) {
            password += characters[getRandomInteger(0, characters.length - 1)];
        }
        characters = '';
        passwordLength = 0;
        return password;
    }
}
