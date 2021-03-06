module.exports = {
    root: true,
    env: {
        node: true,
        "django/i18n": true,
        "es6": true
    },
    plugins: ["django"],
    parserOptions: {
        parser: 'babel-eslint',
        "ecmaVersion": 2017
    },
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'indent': ['error', 4]
    },
};
