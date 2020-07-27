<template>
    <div id="ModifyForm">
        <div v-if="modalVisible">
            <transition name="modal-fade">
                <div class="modal-backdrop">
                    <div>
                        <div class="modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
                            <div>
                                <button type="button" class="btn-close topright" @click="close" aria-label="Close modal">x</button>
                            </div>
                            <header class="modal-header" id="modalTitle">
                                <div>
                                    <h4>Confirm Submit</h4>
                                </div>
                            </header>
                            <section class="modal-body" id="modalDescription">
                                <slot name="body">
                                    <p>Are you sure you want to submit?</p>
                                </slot>
                            </section>
                            <footer class="modal-footer">
                                <div>
                                    <slot name="footer">
                                        <button type="button" class="btn-button" @click="formSubmit">
                                            Yes
                                        </button>
                                        <button type="button" class="btn-button" @click="close">
                                            No
                                        </button>
                                    </slot>
                                </div>
                            </footer>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
        <div class="panel">
            <div class="panel-heading"><h4>Modify Form</h4></div>
            <div class="panel-body">
                <h4 class="sectionHeading">{{formName}} Form</h4>
                <hr />
                <form v-on:submit="showModal">
                    <label for="formName">Form Name:</label>
                    <input type="text" id="formName" name="formName" v-model="formName" required />
                    <label for="formKey">Form Key:</label>
                    <input type="text" id="formKey" name="formKey" v-model="formData.FormKey" v-bind:disabled="formKey != null" required />
                    <label for="actionLink">Action Link:</label>
                    <input type="text" id="actionLink" name="actionLink" v-model="formData.ActionLink" required />
                    <label for="formSchema">Field Schema</label>
                    <br />
                    <textarea id="formSchema" v-model="formData.FieldSchema" required></textarea>
                    <button type="button" @click="updateFieldSchema" class="btn-button">Refresh Form</button>
                    <br />
                    <button type="submit" class="btn-button">Submit</button>
                </form>
                <hr />
                <h4 class="sectionHeading">Form View</h4>
                <vue-form-generator v-if="loaded" :schema="schema" :model="model"></vue-form-generator>
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
                isNewForm: false,
                newFormKey: '',
                newFormAction: '',
                modalVisible: false,
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
                if (this.formKey != null && this.formKey != '')
                    this.fetchData();
                else {
                    this.loaded = true;
                    this.isNewForm = true;
                }
            }
        },
        created: function () {
            if (this.formKey != null && this.formKey != '')
                this.fetchData();
            else {
                this.loaded = true;
                this.isNewForm = true;
            }
        },
        methods: {
            fetchData() {
                if (this.formKey != null && this.formKey != '') {
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
                var json = document.getElementById('formSchema').value;
                console.log(json);

                if (json) {
                    json = JSON.parse(json)
                    this.formData.FieldSchema = json;
                    console.log(this.formData.FieldSchema);
                    this.schema = json;
                    console.log(this.schema);
                }
                else {
                    var newJson = document.getElementById('formSchema').value;
                    this.formData.FieldSchema = JSON.parse(newJson);
                    this.schema = JSON.parse(newJson);
                }
            },
            updateFieldSchema() {
                this.clearWhitespace();
                this.prettyJSON();
            },
            formSubmit() {
                this.modalVisible = false;

                this.formData.FieldSchema = this.schema;

                var data = this.formData;
                var userId = this.$store.getters.userId;
                var isNew = this.isNewForm;
                var formName = this.formName;

                if (this.isNewForm) {
                    var formKey = document.getElementById('formKey').value;
                    var actionLink = document.getElementById('actionLink').value;

                    data = { "FormKey": formKey, "FieldSchema": this.schema, "ActionLink": actionLink, "IsActive": false }
                }

                this.$store.dispatch('updateForm', { data, userId, isNew, formName })
                    .then(resp => { resp.statusText == "OK" ? this.$message("Success") : this.$message("Error"); this.fetchData(); })
                    .catch(err => console.log(err));

                event.preventDefault();
            },
            showModal() {
                this.modalVisible = true;
                event.preventDefault();
            },
            close() {
                this.modalVisible = false;
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

    .modal-backdrop {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: rgba(0, 0, 0, 0.3);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 3;
    }

    .modal {
        background: #FFFFFF;
        box-shadow: 2px 2px 20px 1px;
        overflow-x: auto;
        display: flex;
        flex-direction: column;
        width: 100%;
        border-radius: 5px;
    }

    .modal-header,
    .modal-footer {
        padding-left: 10px;
        display: flex;
        text-align: center;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }

    .modal-header {
        border-bottom: 1px solid #eeeeee;
        color: #479194;
        justify-content: space-between;
    }

    .modal-footer {
        border-top: 1px solid #eeeeee;
        justify-content: center;
    }

    .modal-body {
        position: relative;
        padding: 20px 10px;
    }

    .topright {
        position: initial;
        margin-left: 90%;
        margin-right: 0;
        margin-top: 2px;
    }
</style>