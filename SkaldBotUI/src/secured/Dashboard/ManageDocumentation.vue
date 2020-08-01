<template>
    <div>
        <VueLoading v-if="!loaded"></VueLoading>
        <HelpDocumentation v-if="isModalVisible" :HelpContentKey="helpContentKey" @close="closeModal"></HelpDocumentation>
        <div v-if="loaded">
            <div style="margin-bottom: 10px">
                <el-row>
                    <el-col :span="6">
                        <el-input placeholder="Filter Item Type" v-model="filters[0].value"></el-input>
                    </el-col>
                </el-row>
            </div>

            <data-tables :data="data" :action-col="actionCol" :filters="filters" @selection-change="handleSelectionChange">
                <el-table-column v-for="title in titles" :prop="title.prop" :label="title.label" :key="title.prop" sortable="custom">
                </el-table-column>
                <el-table-column prop="IsActive" label="Is Active">
                    <template slot-scope="scope">
                        <div>{{getBool(scope.row.IsActive)}}</div>
                    </template>
                </el-table-column>
            </data-tables>
        </div>
    </div>
</template>

<script>
    // fake server
    import VueLoading from '../../components/VueLoading';
    import HelpDocumentation from '../../components/HelpDocumentation';

    export default {
        name: "ManageDocumentation",
        components: {
            VueLoading,
            HelpDocumentation
        },
        data() {
            return {
                helpContentKey: '',
                loaded: false,
                isModalVisible: false,
                data: [],
                titles: [
                    {
                        prop: "HelpContentKey",
                        label: "Help Content Key"
                    },
                    {
                        prop: "HelpTitle",
                        label: "Help Title"
                    }
                ],
                filters: [
                    {
                        prop: 'HelpTitle',
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
                                this.helpContentKey = row.HelpContentKey
                                this.showModal();
                            },
                            label: 'View'
                        }
                    ]
                },
                selectedRow: []
            }
        },
        mounted: function () {
            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
            else {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                    this.$router.push('/unauthorized')
                }
                else {
                    this.isLoaded = true
                    this.getData();
                }
            }
        },
        created: function () {
            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
            else {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                    this.$router.push('/unauthorized')
                }
                else {
                    this.isLoaded = true
                    this.getData();
                }
            }
        },
        methods: {
            getData() {
                this.loaded = false;

                this.$store.dispatch('getAllDocumentation').then(() => {
                    this.data = this.$store.getters.helpDocumentation
                    this.loaded = true
                }).catch((err) => {
                    console.log(err)
                    this.$message("There was an error getting the help documentations")
                })
            },
            handleSelectionChange(val) {
                this.selectedRow = val
            },
            getBool(value) {
                if (value)
                    return "True"
                else
                    return "False"
            },
            showModal() {
                this.isModalVisible = true
            },
            closeModal() {
                this.isModalVisible = false;
                this.helpContentKey = '';
                this.getData();
            },
            reloadAuthentication() {
                this.$store.dispatch('loadRoles').then(() => {
                    if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                        this.$router.push('/unauthorized')
                    }
                    else {
                        this.isLoaded = true
                        this.getData();
                    }
                });
            }
        }
    }
</script>