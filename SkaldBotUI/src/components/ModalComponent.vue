<template>
    <div id="Modal">
        <modal v-if="isLoaded && isSuggestion" @close="closeModal">
            <template #title>
                <p>{{lookupData[0].Title}}</p>
            </template>
            <template #body>
                <vue-input id="itemType" name="itemType" v-model="lookupData[0].ItemType" :is-disabled="true">Suggestion Type</vue-input>
                <vue-text-area id="itemText" name="itemText" v-model="lookupData[0].ItemText" :is-disabled="true">Content</vue-text-area>
                <hr />
                <vue-input id="serverId" name="serverId" v-model="lookupData[0].ServerId" :is-disabled="true">Server ID</vue-input>
                <vue-input id="dateCreated" name="dateCreated" :value="getDate(lookupData[0].CreateDate)" :is-disabled="true">Date Submitted</vue-input>
                <vue-input id="discordUserId" name="discordUserId" v-model="lookupData[0].DiscordUserId" :is-disabled="true">Submitted By</vue-input>
            </template>
            <template #actionButtons>
                <vue-button type="button" @click="approveSuggestion">
                    Approve
                </vue-button>
                <vue-button type="button" varient="danger" @click="rejectSuggestion">
                    Reject
                </vue-button>
            </template>
        </modal>
        <modal v-if="isLoaded && !isSuggestion" @close="closeModal">
            <template #title>
                <p v-if="isStory">Manage Story</p>
                <p v-if="isWisdom">Manage Wisdom</p>
            </template>
            <template #body>
                <vue-input v-if="isStory" id="title" name="title" v-model="lookupData[0].Title">Title</vue-input>
                <vue-text-area v-if="isStory" id="itemText" name="itemText" v-model="lookupData[0].Story">Content</vue-text-area>
                <vue-text-area v-if="isWisdom" id="itemText" name="itemText" v-model="lookupData[0].Wisdom">Content</vue-text-area>
                <vue-input id="serverId" name="serverId" v-model="lookupData[0].luS[0].ServerId">Server ID</vue-input>
                <vue-checkbox id="isActive" name="isActive" v-model="lookupData[0].IsActive">Is Active</vue-checkbox>
            </template>
            <template #actionButtons>
                <vue-button type="button" @click="saveItem">
                    Save
                </vue-button>
                <vue-button type="button" varient="danger" @click="closeModal">
                    Close
                </vue-button>
            </template>
        </modal>
    </div>
</template>

<script>
    import VueLoading from '../components/VueLoading';
    import UtilMixin from '@/mixins/util-mixin'
    import PageMixin from '@/mixins/page-mixin'
    import Modal from '@/components/Modal/Modal.vue';
    import fieldInput from '@/components/CustomFields/fieldInput.vue';
    import fieldCheckbox from '@/components/CustomFields/fieldCheckbox.vue';
    import fieldTextArea from '@/components/CustomFields/fieldTextArea.vue';
    import fieldButton from '@/components/CustomFields/fieldButton.vue';

    export default {
        name: 'ModalForm',

        components: {
            VueLoading,
            'modal': Modal,
            'vue-input': fieldInput,
            'vue-checkbox': fieldCheckbox,
            'vue-text-area': fieldTextArea,
            'vue-button': fieldButton
        },

        mixins: [PageMixin, UtilMixin],

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

        computed: {
            isSuggestion() {
                return this.modalDisplayTypeId == 1;
            },

            isStory() {
                return this.modalDisplayTypeId == 2;
            },

            isWisdom() {
                return this.modalDisplayTypeId == 3;
            }
        },

        watch: {
            lookupId() {
                this.getData();
            }
        },

        methods: {
            approveSuggestion() {
                let postData = { "IsApproved": 1, "Id": this.lookupId, "UserId": this.$store.getters.userId }

                this.submitSuggestionChange(postData);
            },

            rejectSuggestion() {
                let postData = { "IsApproved": 0, "Id": this.lookupId, "UserId": this.$store.getters.userId }

                this.submitSuggestionChange(postData);
            },

            submitSuggestionChange(postData) {
                this.$store.dispatch('updateSuggestionState', postData).then(() => {
                    var returnVal = this.$store.getters.getSubmittedResponse;
                    if (returnVal == "Success") {
                        let that = this;
                        this.success("Successfully updated submitted item!");
                        this.closeModal();
                    }
                    else {
                        this.error("Error updating submitted item!");
                    }
                }).catch(err => {
                    this.error("Error updating submitted item!");
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
                                this.error("There was an error getting the suggestion data");
                            })
                            break;
                        case 2:
                            //Get story information
                            this.$store.dispatch('getStoryData', lookupId).then(() => {
                                this.lookupData = this.$store.getters.getStory;
                                this.isLoaded = true;
                            }).catch(err => {
                                console.log(err);
                                this.error("There was an error getting the story data");
                            })
                            break;
                        case 3:
                            //Get wisdom information
                            this.$store.dispatch('getWisdomData', lookupId).then(() => {
                                this.lookupData = this.$store.getters.getWisdom;
                                this.isLoaded = true;
                            }).catch(err => {
                                console.log(err);
                                this.error("There was an error getting the wisdom data");
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
                                this.success("Successfully updated story!");
                                this.closeModal();
                            }
                            else {
                                this.error("Error updating story!");
                            }
                        }).catch(err => {
                            this.error("Error updating story!");
                        })
                        break;
                    case 3:
                        var wisdom = this.lookupData;
                        this.$store.dispatch('updateWisdom', wisdom).then(() => {
                            var returnVal = this.$store.getters.getSubmittedResponse;
                            let that = this;
                            if (returnVal == "Success") {
                                this.success("Successfully updated wisdom!");
                                this.closeModal();
                            }
                            else {
                                this.error("Error updating wisdom!");
                            }
                        }).catch(err => {
                            this.error("Error updating wisdom!");
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