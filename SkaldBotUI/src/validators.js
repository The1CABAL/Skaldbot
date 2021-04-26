import VueFormGenerator from 'vue-form-generator'

VueFormGenerator.validators.emailValidation = function (value, field, model) {
    let email = model.email;
    let confEmail = value;

    if (email != confEmail) {
        return ["Emails do not match!"];
    } else {
        return [];
    }
}

VueFormGenerator.validators.passwordStrength = function (value, field, model) {
    let regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/

    let password = model.password;

    if (!regex.test(password)) {
        return ["Password must be a minimum of eight characters and have at least one letter and one number"]
    }
    else {
        return [];
    }
}

VueFormGenerator.validators.passwordValidation = function (value, field, model) {
    let password = model.password;

    let confPassword = value;

    if (password != confPassword) {
        return ["Passwords do not match!"];
    }
    else {
        return [];
    }
}