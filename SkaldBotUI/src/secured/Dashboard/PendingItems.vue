<template>
    <div>
        <VueLoading v-if="!loaded"></VueLoading>
        <Modal v-show="isModalVisible" @close="closeModal" v-bind:modalDisplayTypeId="modalDisplayTypeId" v-bind:lookupId="lookupId"></Modal>
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
                <el-table-column prop="IsApproved" label="Is Approved">
                    <template slot-scope="scope">
                        <div>{{getBool(scope.row.IsApproved)}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="IsReviewed" label="Is Reviewed">
                    <template slot-scope="scope">
                        <div>{{getBool(scope.row.IsReviewed)}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="CreateDate" label="Date Created">
                    <template slot-scope="scope">
                        <div>{{getDate(scope.row.CreateDate)}}</div>
                    </template>
                </el-table-column>
            </data-tables>
        </div>
    </div>
</template>

<script>
    // fake server
    import VueLoading from '../../components/VueLoading';
    import axios from 'axios';
    import { BaseUrl } from '../../helpers/constants';
    import Modal from '../../components/ModalComponent';

    export default {
        name: "PendingItems",
        components: {
            VueLoading,
            Modal
        },
        data() {
            return {
                modalDisplayTypeId: 1,
                lookupId: 0,
                loaded: false,
                isModalVisible: false,
                data: [],
                titles: [
                    {
                        prop: "Id",
                        label: "Submitted Item Id"
                    },
                    {
                        prop: "ItemType",
                        label: "Submitted Item Type"
                    },
                    {
                        prop: "Title",
                        label: "Title"
                    }
                ],
                filters: [
                    {
                        prop: 'ItemType',
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
                let userUrl = BaseUrl + "submittedItems";
                var that = this;
                axios.get(userUrl).then(function (response) {
                    if (response.data.length > 0) {
                        that.data = JSON.parse(response.data);
                        for (var i = 0; i < that.data.length; i++) {
                            that.data[i].ItemType = that.data[i].luIT[0].ActualItemType
                        }
                    }
                }).catch(function (error) {
                    console.log(error);
                    that.$message('There was an error getting the submitted items')
                });
                that.loaded = true;
            },
            handleSelectionChange(val) {
                this.selectedRow = val
            },
            getDate(date) {
                let elDate = new Date(date)
                return (elDate.getMonth() + 1) + '-'
                    + elDate.getDate() + '-'
                    + elDate.getFullYear()
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