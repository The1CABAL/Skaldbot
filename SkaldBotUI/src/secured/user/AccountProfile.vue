<template>
    <div id="AccountProfile">
        <div class="pb-3">
            <vue-button @click="goBack">Go Back</vue-button>
        </div>
        <div v-if="submitted" v-bind:class="isError ? 'errorMsg' : 'successMsg'">
            <p style="font-weight: bold;">{{msg}}</p>
            <vue-button varient="close" @click="closeNotification">x</vue-button>
        </div>
        <tabs>
            <tab title="Account Information">
                <div class="panel">
                    <div class="panel-heading"><h4 class="font-bold tracking-wide">Account Profile</h4></div>
                    <div class="panel-body">
                        <h4 class="font-bold tracking-wide">{{accountData.AccountName}}</h4>
                        <hr class="mt-3" />
                        <form v-on:submit="formSubmit">
                            <vue-input name="accountName" id="accountName" v-model="accountData.AccountName">Account Name</vue-input>
                            <vue-input name="createDate" id="createDate" :value="getDate(accountData.CreateDate)" :is-disabled="true">Date Created</vue-input>
                            <vue-checkbox v-model="accountData.IsActive">Is Active</vue-checkbox>
                            <vue-button type="submit">Save</vue-button>
                        </form>
                    </div>
                </div>
            </tab>
            <tab title="Users" class="panel p-3">
                <vue-button v-on:click="registerUser">Add User</vue-button>
                <vue-table-filtered :hidden-columns="['Id']"
                                    showPerPage
                                    showSearchField
                                    showPagination
                                    :items="accountUsers"
                                    :pages="1"
                                    @editClick="handleSelectionChange">
                    <vue-table-column v-for="title in titles" :label="title.label" :key="title.prop" is-sortable />
                    <vue-table-column label="User Active" is-sortable />
                    <vue-table-column label="User Locked" is-sortable />
                    <vue-table-column prop="CreateDate" label="Date Created" is-sortable />
                </vue-table-filtered>
            </tab>
        </tabs>
    </div>
</template>

<script>
    import fieldButton from '../../components/CustomFields/fieldButton'
    import fieldCheckbox from '../../components/CustomFields/fieldCheckbox'
    import fieldInput from '../../components/CustomFields/fieldInput'
    import vueTableFiltered from '../../components/Tables/vueTableFiltered'
    import vueTableColumn from '../../components/Tables/vueTableColumn'
    import PageMixin from '@/mixins/page-mixin.js'
    import UtilMixin from '@/mixins/util-mixin.js'

    export default {
        name: "AccountProfile",

        props: {
            accountId: {
                type: String,
                required: true
            }
        },

        mixins: [PageMixin, UtilMixin],

        components: {
            'vue-button': fieldButton,
            'vue-checkbox': fieldCheckbox,
            'vue-input': fieldInput,
            'vue-table-filtered': vueTableFiltered,
            'vue-table-column': vueTableColumn
        },

        data() {
            return {
                accountData: [],
                accountUsers: [],
                msg: '',
                isError: true,
                submitted: false,
                success: false,
                titles: [
                    {
                        prop: "Username",
                        label: "Username"
                    },
                    {
                        prop: "FirstName",
                        label: "First Name"
                    },
                    {
                        prop: "LastName",
                        label: "Last Name"
                    }
                ],
                filters: [
                    {
                        prop: 'Username',
                        value: ''
                    }
                ],
                actionCol: {
                    props: {
                        label: 'Actions',
                    },
                    buttons: [
                        {
                            props:
                            {
                                type: 'primary'
                            },
                            handler: row => {
                                this.userId = row.Id
                                this.$router.push('/userprofile/' + this.userId)
                            },
                            label: 'Edit'
                        }
                    ]
                }
            }
        },

        watch: {
            submitted: function () {
                if (this.submitted) {
                    setTimeout(this.closeNotification, 5000);
                }
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                this.getData().then(() => {
                    if (!this.masterAdmin && !this.admin && !this.clientAdmin) {
                        this.$router.push('/unauthorized')
                    }

                    this.pageReady();
                });
            });
        },

        computed: {
            hasAccountUsers() {
                return this.accountUsers.length > 0;
            }
        },

        methods: {
            formSubmit() {
                event.preventDefault();
                if (!this.objectsAreSame(this.accountData, this.$store.getters.accountInformation)) {
                    let that = this;
                    this.$store.dispatch('updateAccountInformation', this.accountData).then(() => {
                        that.success = true
                        that.setNotification(that.success);
                        that.getData()
                    }).catch(err => {
                        that.success = false;
                        that.setNotification(that.success)
                        that.getData()
                        console.log(err);
                    })
                }
                else {
                    this.setNotification(false);
                }
            },

            setNotification(success) {
                if (success) {
                    this.submitted = true;
                    this.isError = false;
                    this.msg = "Successfully updated the account!";
                }
                else {
                    this.submitted = true;
                    this.isError = true;
                    this.msg = "There was an error updating the account. Please try again.";
                }
            },

            closeNotification() {
                this.msg = '';
                this.submitted = false;
                this.isError = false;
            },

            async getData() {
                await this.getAccountInformation();
                //await this.getAccountUsers();
            },

            async getAccountInformation() {
                let accountId = this.accountId;
                let masterAdmin = this.masterAdmin;
                let that = this;

                this.$store.dispatch('getAccountInformation', { accountId, masterAdmin }).then(() => {
                    that.accountData = { ...this.$store.getters.accountInformation };
                    that.accountUsers = this.$store.getters.accountUsers;
                }).catch(err => {
                    that.$message('Error loading account data!');
                    console.log(err);
                })
            },

            async getAccountUsers() {
                let accountId = this.accountId;
                let masterAdmin = this.masterAdmin;

                this.$store.dispatch('getAccountUsers', { accountId, masterAdmin }).then(() => {
                    that.accountUsers = this.$store.getters.accountUsers;
                }).catch(err => {
                    that.$message('Error loading account data!');
                    console.log(err);
                })
            },

            objectsAreSame(x, y) {
                return this.areEquivalient(x, y)
            },

            goBack() {
                this.redirectUser(this.prevRoute.path)
            },

            handleSelectionChange(val) {
                this.redirectUser(`/userprofile/${val}`)
            },

            registerUser() {
                this.redirectUser(`/registerUser/${this.accountId}`);
            }
        }
    }
</script>

<style scoped>
</style>