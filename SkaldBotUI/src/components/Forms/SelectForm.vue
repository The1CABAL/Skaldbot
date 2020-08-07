<template>
    <div class="selectsuggestion">
        <div>
            <select @change="setKey($event)" class="select-css">
                <option value="select">Select</option>
                <option v-for="form in getForms" :key="form.FormKey" :value="form.FormKey">{{form.FormName}}</option>
            </select>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapActions } from "vuex";

    export default {
        name: "SelectForm",
        props: ['pageId'],
        data() {
            return {
                formKey: '',
                thePageId: { ...this.pageId }
            }
        },
        methods: {
            ...mapActions(["fetchAllForms", "fetchAllFormsByPageId"]),
            setKey(e) {
                const key = e.target.options[e.target.options.selectedIndex].value;

                if (key == "select") {
                    this.formKey = key;
                    this.$emit('formKey', '');
                }
                else {
                    this.formKey = key;
                    this.$emit('formKey', key);
                }
            }
        },
        computed: mapGetters(["getForms"]),
        created() {
            if (this.pageId == 0 || this.pageId == undefined)
                this.fetchAllForms();
            else {
                this.fetchAllFormsByPageId(this.pageId);
            }
        }
    }
</script>

<style scoped>
</style>