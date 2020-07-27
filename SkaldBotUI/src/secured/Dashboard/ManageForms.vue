<template>
    <div id="ManageForms">
        <VueLoading v-if="!loaded"></VueLoading>
        <div v-if="loaded">
            <div style="margin-bottom: 10px">
                <el-row>
                    <el-col :span="6">
                        <el-input placeholder="Form Name..." v-model="filters[0].value"></el-input>
                        <button type="button" @click="newForm">New Form</button>
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
    import axios from 'axios';
    import { BaseUrl } from '../../helpers/constants';

    export default {
        name: "ManageForms",
        components: {
            VueLoading
        },
        data() {
            return {
                loaded: false,
                data: [],
                titles: [
                    {
                        prop: "FormKey",
                        label: "Form Key"
                    },
                    {
                        prop: "FormName",
                        label: "Form Name"
                    }
                ],
                filters: [
                    {
                        prop: 'FormName',
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
                                //this.$message("This feature is not yet implemented");
                                this.$router.push('/modifyform/' + row.FormKey)
                            },
                            label: 'View'
                        }
                    ]
                },
                selectedRow: []
            }
        },
        mounted: function () {
            this.fetchData();
        },
        created: function () {
            if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                this.$router.push('/unauthorized')
            }
            else {
                this.fetchData()
            }
        },
        methods: {
            fetchData() {
                return this.$store.dispatch('fetchAllForms').then(() => {
                    this.getData();
                });
            },
            getData() {
                this.data = this.$store.getters.allForms
                this.loaded = true;
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
            newForm() {
                this.$router.push('/modifyform')
            }
        }
    }
</script>

<style scoped>
</style>