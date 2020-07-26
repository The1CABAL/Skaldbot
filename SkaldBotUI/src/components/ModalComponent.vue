<template>
    <div id="Modal">
        <transition name="modal-fade">
            <VueLoading v-if="!isLoaded"></VueLoading>
            <div class="modal-backdrop" v-if="isLoaded">
                <div v-if="modalDisplayTypeId == 1">
                    <div class="modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
                        <div>
                            <button type="button" class="btn-close topright" @click="close" aria-label="Close modal">x</button>
                        </div>
                        <header class="modal-header" id="modalTitle">
                            <div>
                                <h4>{{lookupData[0].Title}}</h4>
                            </div>
                        </header>
                        <section class="modal-body" id="modalDescription">
                            <slot name="body">
                                <label for="itemType">Suggestion Type:</label>
                                <input type="text" id="itemType" v-model="lookupData[0].ItemType" disabled />
                                <label for="itemText">Content:</label>
                                <textarea id="itemText" disabled>{{lookupData[0].ItemText}}</textarea>
                                <hr />
                                <label for="dateCreated">Date Submitted:</label>
                                <input type="text" id="dateCreated" :value="getDate(lookupData[0].CreateDate)" disabled />
                                <label for="submitterEmail">Submitted By:</label>
                                <input type="email" id="submitterEmail" v-model="lookupData[0].SubmitterEmail" disabled />
                            </slot>
                        </section>
                        <footer class="modal-footer">
                            <div>
                                <slot name="footer">
                                    <button type="button" class="btn-button approve" @click="approveSuggestion">
                                        Approve
                                    </button>
                                    <button type="button" class="btn-button reject" @click="rejectSuggestion">
                                        Reject
                                    </button>
                                </slot>
                            </div>
                        </footer>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
    import VueLoading from '../components/VueLoading';
    import axios from 'axios';
    import { BaseUrl } from '../helpers/constants';

    export default {
        name: 'Modal',
        components: {
            VueLoading
        },
        props: {
            modalDisplayTypeId: {
                type: Number,
                required: false
            },
            lookupId: {
                type: Number,
                required: false
            }
        },
        data() {
            return {
                isLoaded: false,
                lookupData: {}
            }
        },
        watch: {
            lookupId: function () {
                if (this.lookupId != 0) {
                    let id = this.modalDisplayTypeId;
                    switch (id) {
                        case 1:
                            //Lookup suggested item
                            let url = BaseUrl + "submititem?id=" + this.lookupId;
                            var that = this;
                            axios.get(url).then(function (response) {
                                that.lookupData = JSON.parse(response.data);
                                that.lookupData[0].ItemType = that.lookupData[0].luIT[0].ItemType
                                that.isLoaded = true;
                            }).catch(function (error) {
                                console.log(error);
                                that.$message("There was an error getting the suggestion data");
                            });
                    }
                }
            }
        },
        methods: {
            close() {
                this.$emit('close');
            },
            getDate(date) {
                let elDate = new Date(date)
                return (elDate.getMonth() + 1) + '-'
                    + elDate.getDate() + '-'
                    + elDate.getFullYear()
            },
            approveSuggestion() {
                let url = BaseUrl + 'submittedItems'
                let postData = { "IsApproved": 1, "Id": this.lookupId, "UserId": this.$store.getters.userId }
                let that = this;
                axios.post(url, postData).then(function (response) {
                    var returnVal = response.data;
                    if (returnVal.Message.toString() == "Success") {
                        that.$message('Successfully updated submitted item!');
                        setTimeout(function () {
                            that.close()
                        }, 2000)
                    }
                    else {
                        //console.log("Setting success to false");
                        that.$message('Error updating submitted item!');
                    }
                });
            },
            rejectSuggestion() {
                let url = BaseUrl + 'submittedItems'
                let postData = { "IsApproved": 0, "Id": this.lookupId, "UserId": this.$store.getters.userId }
                let that = this;
                axios.post(url, postData).then(function (response) {
                    var returnVal = response.data;
                    if (returnVal.Message.toString() == "Success") {
                        that.$message('Successfully updated submitted item!');
                        setTimeout(function () {
                            that.close()
                        }, 2000)
                    }
                    else {
                        //console.log("Setting success to false");
                        that.$message('Error updating submitted item!');
                    }
                });
            }
        },
    };
</script>

<style scoped>
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

    .btn-button {
        border: none;
        display: inline-block;
        padding: 8px 16px;
        vertical-align: middle;
        overflow: hidden;
        text-decoration: none;
        color: black;
        background-color: none;
        text-align: center;
        cursor: pointer;
        white-space: nowrap;
        padding: 5px;
        margin: 5px;
        border-radius: 4px;
    }

    .topright {
        position: initial;
        margin-left: 95%;
        margin-right: 0;
        margin-top: 2px;
    }

    input {
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
    }

    .approve {
        background-color: #45DE6A;
    }

    .reject {
        background-color: #DE4547;
    }
</style>