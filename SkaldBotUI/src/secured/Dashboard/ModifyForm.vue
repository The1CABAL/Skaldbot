<template>
    <div id="ModifyForm">
        <div class="panel">
            <div class="panel-heading"><h4>Modify Form</h4></div>
            <div class="panel-body">
                <h4 class="sectionHeading">{{formName}} Form</h4>
                <hr />
                <form>
                    <label for="formName">Form Name:</label>
                    <input type="text" id="formName" name="formName" v-model="formName" />
                    <label for="formKey">Form Key:</label>
                    <input type="text" id="formKey" name="formKey" v-model="formData.FormKey" disabled />
                    <label for="actionLink">Action Link:</label>
                    <input type="text" id="actionLink" name="actionLink" v-model="formData.ActionLink" />
                    <label for="formSchema">Field Schema</label>
                    <br />
                    <textarea id="formSchema" v-model="formData.FieldSchema"></textarea>
                    <button type="button" @click="updateFieldSchema" class="btn-button">Refresh Form</button>
                </form>
                <hr />
                <h4 class="sectionHeading">Form View</h4>
                <vue-form-generator v-if="loaded" :schema="schema" :model="model" disabled></vue-form-generator>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ModifyForm",
        props: {
            formKey: {
                type: String,
                required: false
            }
        },
        data() {
            return {
                loaded: false,
                formName: '',
                formData: [],
                schema: [],
                model: {}
            }
        },
        mounted: function () {
            if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                this.$router.push('/unauthorized')
            }
            else {
                this.fetchData();
            }
        },
        created: function () {
            this.fetchData();
        },
        methods: {
            fetchData() {
                if (this.formKey != '') {
                    return this.$store.dispatch('fetchFormByFormKey', this.formKey).then(() => {
                        this.getData();
                    });
                }
            },
            getData() {
                this.formData = this.$store.getters.getForm
                this.formData = this.formData[0]
                this.formData.FieldSchema = JSON.parse(this.formData.FieldSchema)
                this.schema = this.formData.FieldSchema
                this.formName = this.formData.luVF[0].FormName;
                this.prettyJSON();
                this.loaded = true;
            },
            prettyJSON() {
                var element = document.getElementById('formSchema');
                var json = null;

                if (element != null)
                    json = element.innerHTML;

                if (json) {
                    json = JSON.stringify(json, undefined, 4);
                    this.formData.FieldSchema = json;
                }
                else {
                    var json = this.formData.FieldSchema;
                    json = JSON.stringify(json, undefined, 4);
                    this.formData.FieldSchema = json;
                }
            },
            clearWhitespace() {
                var json = document.getElementById('formSchema').innerHTML;

                if (json) {
                    json = JSON.parse(json)
                    this.formData.FieldSchema = json;
                    this.schema = json;
                }
                else {
                    json = this.formData.FieldSchema;
                    json = JSON.parse(json);
                    this.formData.FieldSchema = json;
                    this.schema = json;
                }
                console.log(json);
            },
            updateFieldSchema() {
                this.clearWhitespace();
                this.prettyJSON();
            }
        }
    }
</script>

<style scoped>
    .btn-button {
        border: 1px solid black;
        display: inline-block;
        padding: 8px 16px;
        vertical-align: middle;
        overflow: hidden;
        text-decoration: none;
        color: black;
        background-color: lightgray;
        text-align: center;
        cursor: pointer;
        white-space: nowrap;
        padding: 5px;
        margin: 5px;
        border-radius: 4px;
    }

    .close {
        position: absolute;
        font-size: 15px;
        top: 1px;
        right: 0;
        border: 0;
        padding-right: 5px;
        background-color: rgba(0,0,0,0.0);
    }

    .successMsg {
        position: relative;
        display: inline-block;
        width: 100%;
        height: auto;
        background: #93FFA1;
        border-radius: 10px 10px 10px 10px;
        overflow: hidden;
        padding-left: 10px;
    }

    .errorMsg {
        position: relative;
        display: inline-block;
        width: 100%;
        height: auto;
        background: #FF9393;
        border-radius: 10px 10px 10px 10px;
        overflow: hidden;
        padding-left: 10px;
    }

    .panel {
        margin-top: 5px;
        margin-bottom: 20px;
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
        padding: 5px 15px;
        border-bottom: 1px solid transparent;
        border-top-left-radius: 3px;
        border-top-right-radius: 3px;
    }

    .panel-body {
        padding: 15px;
        background-color: #fff;
    }

    input[type=text] {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }

    textarea {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
        min-height: 250px;
    }

    .sectionHeading {
        color: #00b1b1;
    }
</style>