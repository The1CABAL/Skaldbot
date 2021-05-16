export default {
    mounted() {
        if (this.schema.onMount) {
            var self = this;
            eval(decodeURI(this.schema.onMount))
        }
    }
}