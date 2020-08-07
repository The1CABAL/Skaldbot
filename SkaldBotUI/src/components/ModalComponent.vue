<template>
    <div id="Modal">
        <transition name="modal-fade">
            <VueLoading v-if="!isLoaded"></VueLoading>
            <div class="modal-backdrop" v-if="isLoaded">
                <div v-if="modalDisplayTypeId == 1">
                    <div class="modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
                        <div>
                            <button type="button" class="btn-close topright" @click="closeModal" aria-label="Close modal">x</button>
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
                                <label for="serverId">Server ID:</label>
                                <input type="text" id="serverId" v-model="lookupData[0].ServerId" disabled />
                                <label for="dateCreated">Date Submitted:</label>
                                <input type="text" id="dateCreated" :value="getDate(lookupData[0].CreateDate)" disabled />
                                <label for="discordUserId">Submitted By:</label>
                                <input type="text" id="discordUserId" v-model="lookupData[0].DiscordUserId" disabled />
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
                            <button type="button" class="btn-close topright" @click="closeModal" aria-label="Close modal">x</button>
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
                                    <label for="serverId">Server ID:</label>
                                    <input type="text" id="serverId" v-model="lookupData[0].luS[0].ServerId"/>
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
                                    <button type="button" class="btn-button" @click="closeModal">
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
            lookupId: function() {
                this.getData();
            }
        },
        methods: {
            getDate(date) {
                let elDate = new Date(date)
                return (elDate.getMonth() + 1) + '-'
                    + elDate.getDate() + '-'
                    + elDate.getFullYear()
            },
            approveSuggestion() {
                //let url = BaseUrl + 'submittedItems'
                let postData = { "IsApproved": 1, "Id": this.lookupId, "UserId": this.$store.getters.userId }

                this.submitSuggestionChange(postData);
                //let that = this;
                //axios.post(url, postData).then(function (response) {
                //    var returnVal = response.data;
                //    if (returnVal.Message.toString() == "Success") {
                //        that.$message('Successfully updated submitted item!');
                //        setTimeout(function () {
                //            that.close()
                //        }, 2000)
                //    }
                //    else {
                //        //console.log("Setting success to false");
                //        that.$message('Error updating submitted item!');
                //    }
                //});
            },
            rejectSuggestion() {
                //let url = BaseUrl + 'submittedItems'
                let postData = { "IsApproved": 0, "Id": this.lookupId, "UserId": this.$store.getters.userId }

                this.submitSuggestionChange(postData);
                //let that = this;
                //axios.post(url, postData).then(function (response) {
                //    var returnVal = response.data;
                //    if (returnVal.Message.toString() == "Success") {
                //        that.$message('Successfully updated submitted item!');
                //        setTimeout(function () {
                //            that.close()
                //        }, 2000)
                //    }
                //    else {
                //        //console.log("Setting success to false");
                //        that.$message('Error updating submitted item!');
                //    }
                //});
            },
            submitSuggestionChange(postData) {
                this.$store.dispatch('updateSuggestionState', postData).then(() => {
                    var returnVal = this.$store.getters.getSubmittedResponse;
                    if (returnVal == "Success") {
                        let that = this;
                        this.$message("Successfully updated submitted item!");
                        setTimeout(function () {
                            that.closeModal();
                        }, 2000)
                    }
                    else {
                        this.$message("Error updating submitted item!");
                    }
                }).catch(err => {
                    console.log(err);
                    this.$message("Error updating submitted item!");
                })
            },
            getData() {
                if (this.lookupId != 0 && this.lookupId != null) {
                    var id = this.modalDisplayTypeId;
                    var lookupId = this.lookupId
                    switch (id) {
                        case 1:
                            //Lookup suggested item
                            this.$store.dispatch('getSubmittedItemData', lookupId).then(() => {
                                this.lookupData = this.$store.getters.getSubmittedItem;
                                this.lookupData[0].ItemType = this.lookupData[0].luIT[0].ItemType
                                this.isLoaded = true;
                            }).catch(err => {
                                console.log(err);
                                this.$message("There was an error getting the suggestion data");
                            })
                            break;
                        case 2:
                            //Get story information
                            this.$store.dispatch('getStoryData', lookupId).then(() => {
                                this.lookupData = this.$store.getters.getStory;
                                this.isLoaded = true;
                            }).catch(err => {
                                console.log(err);
                                this.$message("There was an error getting the story data");
                            })
                            break;
                        case 3:
                            //Get wisdom information
                            this.$store.dispatch('getWisdomData', lookupId).then(() => {
                                this.lookupData = this.$store.getters.getWisdom;
                                this.isLoaded = true;
                            }).catch(err => {
                                console.log(err);
                                this.$message("There was an error getting the wisdom data");
                            })
                            break;
                    }
                }
            },
            saveItem() {
                let that = this;
                switch (this.modalDisplayTypeId) {
                    case 2:
                        var story = this.lookupData;
                        this.$store.dispatch('updateStory', story).then(() => {
                            var returnVal = this.$store.getters.getSubmittedResponse;
                            let that = this;
                            if (returnVal == "Success") {
                                this.$message("Successfully updated story!");
                                setTimeout(function () {
                                    that.closeModal();
                                }, 2000)
                            }
                            else {
                                this.$message("Error updating story!");
                            }
                        }).catch(err => {
                            console.log(err);
                            this.$message("Error updating story!");
                        })
                        break;
                    case 3:
                        var wisdom = this.lookupData;
                        this.$store.dispatch('updateWisdom', wisdom).then(() => {
                            var returnVal = this.$store.getters.getSubmittedResponse;
                            let that = this;
                            if (returnVal == "Success") {
                                this.$message("Successfully updated wisdom!");
                                setTimeout(function () {
                                    that.closeModal();
                                }, 2000)
                            }
                            else {
                                this.$message("Error updating wisdom!");
                            }
                        }).catch(err => {
                            console.log(err);
                            this.$message("Error updating wisdom!");
                        })
                        break;
                }
            },
            closeModal() {
                this.$emit('close');
            },
        },
    };
</script>

<style scoped>
</style>