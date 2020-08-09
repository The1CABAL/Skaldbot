<template>
    <div id="ModifyForm">
        <button type="button" class="btn-button" v-on:click="goBack">Go Back</button>
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
                    <label for="isActive">Is Active</label>
                    <br />
                    <input type="checkbox" id="isActive" name="isActive" v-model="formData.IsActive" v-bind:disabled="formKey == null" />
                    <br />
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
        beforeRouteEnter(to, from, next) {
            next((vm) => {
                vm.prevRoute = from
            })
        },
        methods: {
            fetchData() {
                if (this.formKey != null && this.formKey != '') {
                    return this.$store.dispatch('fetchFormToEdit', this.formKey).then(() => {
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
            },
            goBack() {
                this.$router.push(this.prevRoute.path)
            },
        }
    }
</script>

<style scoped>
</style>