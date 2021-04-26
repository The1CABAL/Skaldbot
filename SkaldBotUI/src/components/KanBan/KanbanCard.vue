<template>
    <div id="KanbanCard">
        <div>
            <div v-if="loading">
                <VueLoading></VueLoading>
            </div>
            <div v-if="!loading">
                <div @click="enableMore">
                    <p>#{{cardInfo.number}} - {{cardInfo.title}}</p>
                </div>
            </div>
        </div>
        <div v-if="showMore">
            <modal @close="closeModal(false)">
                <template #title>
                    <p>#{{cardInfo.number}} - {{cardInfo.title}}</p>
                </template>
                <template #body>
                    <div v-if="loading">
                        <section class="model-body" id="modalDescription">
                            <VueLoading />
                        </section>
                    </div>
                    <div v-if="!loading">
                        <section class="modal-body" id="modalDescription">
                            <vue-input id="cardTitle" name="cardTitle" v-model="cardInfo.title">Title</vue-input>
                            <vue-input id="assigneName" name="assigneName" :value="assignee" :is-disabled="true">Assigned To</vue-input>
                            <vue-input id="dateCreated" name="dateCreated" :value="getDate(cardInfo.created_at)" :is-disabled="true">Date Created</vue-input>
                            <hr />
                            <vue-text-area :id="cardInfo.node_id" v-if="resizeTextarea(cardInfo.node_id)" v-model="cardInfo.body">Description</vue-text-area>
                            <div v-if="hasComments">
                                <hr />
                                <h4 class="font-bold tracking-wide mt-3 mb-3">Comments:</h4>
                                <KanbanComments :commentUrl="cardInfo.comments_url"></KanbanComments>
                            </div>
                        </section>
                    </div>
                </template>
                <template #actionButtons>
                    <vue-button type="button" v-if="!loading" @click="updateCard">
                        Update
                    </vue-button>
                    <vue-button varient="secondary" type="button" @click="viewCard">
                        View
                    </vue-button>
                    <vue-button type="button" varient="danger" @click="closeModal(false)">
                        Close
                    </vue-button>
                </template>
            </modal>
        </div>
    </div>
</template>

<script>
    import KanbanComments from '../KanBan/KanbanComments';
    import VueLoading from '../VueLoading';
    import fieldInput from '@/components/CustomFields/fieldInput'
    import fieldTextArea from '@/components/CustomFields/fieldTextArea'
    import fieldButton from '@/components/CustomFields/fieldButton'
    import UtilMixin from '@/mixins/util-mixin'
    import Modal from '@/components/Modal/Modal'

    export default {
        name: "KanbanCard",

        props: {
            contentUrl: {
                type: String,
                required: true
            }
        },

        mixins: [UtilMixin],

        components: {
            KanbanComments,
            VueLoading,
            'vue-input': fieldInput,
            'vue-text-area': fieldTextArea,
            'vue-button': fieldButton,
            'modal': Modal
        },

        data() {
            return {
                cardInfo: [],
                showMore: false,
                loading: false
            }
        },

        mounted() {
            this.getCardInfo();
        },

        computed: {
            assignee() {
                if (this.cardInfo.assignee.login) {
                    return this.cardInfo.assignee.login;
                }

                return 'Unassigned';
            },

            hasComments() {
                return this.cardInfo.comments != 0;
            }
        },

        methods: {
            async getCardInfo() {
                var url = this.contentUrl;

                await this.$store.dispatch('getCardById', url).then(() => {
                    this.cardInfo = this.$store.getters.getCardInfo;
                }).catch(() => {
                    this.error("Error getting card info for card id " + id);
                })
            },

            enableMore() {
                this.showMore = true;
            },

            closeModal(reload) {
                if (reload) {
                    this.$emit('ReloadGithub', 'Reload');
                }
                this.showMore = false;
            },

            viewCard() {
                window.open(this.cardInfo.html_url, '_blank');
            },

            async updateCard() {
                this.loading = true;
                var title = this.cardInfo.title;
                var body = this.cardInfo.body;
                var assignee = this.cardInfo.assignee.login;
                var state = this.cardInfo.state;
                var mileStone = this.cardInfo.milestone.number;

                var labels = [];
                this.cardInfo.labels.forEach(obj => {
                    Object.entries(obj).forEach(([key, value]) => {
                        if (key == "name") {
                            labels.push(value);
                        }
                    })
                })

                var assignees = [];
                this.cardInfo.assignees.forEach(obj => {
                    Object.entries(obj).forEach(([key, value]) => {
                        if (key == "login") {
                            assignees.push(value);
                        }
                    })
                })

                var updatedCardInfo = { "title": title, "body": body, "assignee": assignee, "state": state, "mileStone": mileStone, "labels": labels, "assignees": assignees };
                var url = this.cardInfo.url;

                var cardData = { url, updatedCardInfo };

                await this.$store.dispatch('updateProjectIssue', cardData).then(() => {
                    this.cardInfo = this.$store.getters.getCardInfo;
                    if (this.$store.getters.getGitHubUpdateMsg == "Success") {
                        this.loading = false;
                        this.success("Updated Issue!");
                    }
                }).catch(() => {
                    this.loading = false;
                    this.error("Error Updating Issue!");
                    this.closeModal(true);
                })
            },

            resizeTextarea(nodeId) {
                setTimeout(function () {
                    var textarea = document.getElementById(nodeId);
                    textarea.style.height = (textarea.scrollHeight) + 2 + 'px';
                }, 50)

                return true;
            }
        }
    }
</script>

<!--<style scoped>
    label {
        color: white;
    }

    .cardText {
        color: white;
    }
</style>-->
