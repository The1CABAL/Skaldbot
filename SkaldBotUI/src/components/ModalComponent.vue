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
                                <br />
                                <textarea id="itemText" v-model="lookupData[0].ItemText" disabled></textarea>
                                <br />
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
                <div v-if="modalDisplayTypeId == 2 || modalDisplayTypeId == 3">
                    <div class="modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
                        <div>
                            <button type="button" class="btn-close topright" @click="close" aria-label="Close modal">x</button>
                        </div>
                        <header class="modal-header" id="modalTitle">
                            <div>
                                <h4 v-if="modalDisplayTypeId == 2">Manage Story</h4>
                                <h4 v-if="modalDisplayTypeId == 3">Manage Wisdom</h4>
                            </div>
                        </header>
                        <section class="modal-body" id="modalDescription">
                            <slot name="body">
                                <div>
                                    <label for="title">Title:</label>
                                    <input type="text" id="title" v-model="lookupData[0].Title" />
                                    <label for="itemText">Content:</label>
                                    <br />
                                    <textarea id="itemText" v-if="modalDisplayTypeId == 2" v-model="lookupData[0].Story" class="modal-textarea"></textarea>
                                    <textarea id="itemText" v-if="modalDisplayTypeId == 3" v-model="lookupData[0].Wisdom" class="modal-textarea"></textarea>
                                    <br />
                                    <label for="isActive">Is Active:</label>
                                    <input type="checkbox" id="isActive" v-model="lookupData[0].IsActive" />
                                </div>
                            </slot>
                        </section>
                        <footer class="modal-footer">
                            <div>
                                <slot name="footer">
                                    <button type="button" class="btn-button approve" @click="saveItem">
                                        Save
                                    </button>
                                    <button type="button" class="btn-button" @click="close">
                                        Close
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
                if (this.lookupId != 0 && this.lookupId != null) {
                    let id = this.modalDisplayTypeId;
                    switch (id) {
                        case 1:
                            //Lookup suggested item
                            let itemUrl = BaseUrl + "submititem?id=" + this.lookupId;
                            var that = this;
                            axios.get(itemUrl).then(function (response) {
                                that.lookupData = JSON.parse(response.data);
                                that.lookupData[0].ItemType = that.lookupData[0].luIT[0].ItemType
                                that.isLoaded = true;
                            }).catch(function (error) {
                                console.log(error);
                                that.$message("There was an error getting the suggestion data");
                            });
                        case 2:
                            //Get story information
                            let storyUrl = BaseUrl + "story?id=" + this.lookupId;
                            var that = this;
                            axios.get(storyUrl).then(function (response) {
                                that.lookupData = JSON.parse(response.data);
                                that.isLoaded = true;
                            }).catch(function (error) {
                                console.log(error);
                                that.$message("There was an error getting the story data");
                            });
                        case 3:
                            //Get wisdom information
                            let wisdomUrl = BaseUrl + "wisdom?id=" + this.lookupId;
                            var that = this;
                            axios.get(wisdomUrl).then(function (response) {
                                that.lookupData = JSON.parse(response.data);
                                that.isLoaded = true;
                            }).catch(function (error) {
                                console.log(error);
                                that.$message("There was an error getting the wisdom data");
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
            },
            saveItem() {
                let that = this;
                switch (this.modalDisplayTypeId) {
                    case 2:
                        let storyUrl = BaseUrl + 'story'
                        axios.post(storyUrl, this.lookupData).then(function (response) {
                            var returnVal = response.data;
                            if (returnVal.Message.toString() == "Success") {
                                that.$message('Successfully updated story!');
                                setTimeout(function () {
                                    that.close()
                                }, 2000)
                            }
                            else {
                                //console.log("Setting success to false");
                                that.$message('Error updating story!');
                            }
                        });
                    case 3:
                        let wisdomUrl = BaseUrl + 'wisdom'
                        axios.post(wisdomUrl, this.lookupData).then(function (response) {
                            var returnVal = response.data;
                            if (returnVal.Message.toString() == "Success") {
                                that.$message('Successfully updated wisdom!');
                                setTimeout(function () {
                                    that.close()
                                }, 2000)
                            }
                            else {
                                //console.log("Setting success to false");
                                that.$message('Error updating wisdom!');
                            }
                        });
                }
            }
        },
    };
</script>

<style scoped>
</style>