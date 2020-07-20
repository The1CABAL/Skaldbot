<template>
    <div class="form">
        <div class="panel">
            <div class="panel-heading">Details</div>
            <hr />
            <div class="panel-body">
                <form action="" v-on:submit.prevent>
                    <vue-form-generator :schema="schema" :model="model"></vue-form-generator>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import Vue from 'vue'
    import VueFormGenerator from "vue-form-generator";
    import "vue-form-generator/dist/vfg.css";  // optional full css additions
    import { mapGetters, mapActions } from "vuex";

    Vue.use(VueFormGenerator)

    export default {
        name: "Form",
        props: {
            formKey: {
                type: String,
                required: true
            }
        },
        mounted: function () {
            let url = "http://127.0.0.1:5000/api" + "/getFormSchema?formKey=" + this.formKey;
            var that = this;
            axios.get(url).then(function (response) {
                that.schema = JSON.parse(response.data);
            });

        },
        watch: {
            formKey: function () {
                console.log("Watching key" + this.formKey);
                let url = "http://127.0.0.1:5000/api" + "/getFormSchema?formKey=" + this.formKey;
                var that = this;
                axios.get(url).then(function (response) {
                    that.schema = JSON.parse(response.data);
                }).catch(error => { this.$emit('error', true) });
            }
        },
        data() {
            return {
                model: {},
                schema: null,
                options: {
                    validatedAfterLoad: false,
                    validatedAfterChange: true
                }
            }
        },
        methods: {
            ...mapActions(["fetchFormData"])
        },
        computed: {
            ...mapGetters(["formSchema"])
        }
    }
</script>

<style scoped>
    .form{
        padding-top: 15px;
    }
    .panel {
        margin-bottom: 20px;
        background-color: #fff;
        border: 1px solid transparent;
        border-radius: 4px;
        -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, .05);
        box-shadow: 0 1px 1px rgba(0, 0, 0, .05);
        border-color: #ddd;
    }

    .panel-heading {
        color: #333;
        background-color: #f5f5f5;
        border-color: #ddd;
        padding: 10px 15px;
        border-bottom: 1px solid transparent;
        border-top-left-radius: 3px;
        border-top-right-radius: 3px;
    }

    .panel-body {
        padding: 15px;
    }
</style>