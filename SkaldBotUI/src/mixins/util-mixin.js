export default {
    methods: {
        debounce(func, wait, immediate) {
            var timeout;
            return function () {
                var context = this, args = arguments;
                var later = function () {
                    timeout = null;
                    if (!immediate) func.apply(context, args);
                };
                var callNow = immediate && !timeout;
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                if (callNow) func.apply(context, args);
            };
        },

        getDate(date) {
            let elDate = new Date(date)
            return (elDate.getMonth() + 1) + '-'
                + elDate.getDate() + '-'
                + elDate.getFullYear()
        },

        getTrueString(value) {
            if (value)
                return "True"
            else
                return "False"
        },
    }
}