<template>
    <div id="ManageWisdoms">
        <VueLoading v-if="!loaded"></VueLoading>
        <Modal v-show="isModalVisible" @close="closeModal" v-bind:modalDisplayTypeId="modalDisplayTypeId" v-bind:lookupId="lookupId"></Modal>
        <div v-if="loaded">
            <div style="margin-bottom: 10px">
                <el-row>
                    <el-col :span="6">
                        <el-input placeholder="Wisdom..." v-model="filters[0].value"></el-input>
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
    import VueLoading from '../../components/VueLoading';
    import Modal from '../../components/ModalComponent';

    export default {
        name: "ManageWisdoms",
        components: {
            VueLoading,
            Modal
        },
        data() {
            return {
                modalDisplayTypeId: 3,
                lookupId: 0,
                loaded: false,
                isModalVisible: false,
                data: [],
                titles: [
                    {
                        prop: "Id",
                        label: "Wisdom Id"
                    },
                    {
                        prop: "Wisdom",
                        label: "Wisdom"
                    }
                ],
                filters: [
                    {
                        prop: 'Wisdom',
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
                                this.lookupId = row.Id
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
        methods: {
            getData() {
                this.loaded = false;
                this.$store.dispatch('getAllWisdoms').then(() => {
                    this.data = this.$store.getters.getWisdoms;
                    this.loaded = true
                }).catch(err => {
                    console.log(err);
                    this.$message("Error getting wisdoms");
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
                this.lookupId = 0;
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

<style scoped>
</style>