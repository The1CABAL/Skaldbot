<template>
    <div id="KanbanCard">
        <div>
            <div v-if="loading">
                <VueLoading></VueLoading>
            </div>
            <div v-if="!loading">
                <div v-if="!showMore" @click="enableMore">
                    <p>#{{cardInfo.number}} - {{cardInfo.title}}</p>
                </div>
            </div>
        </div>
        <div v-if="showMore">
            <transition name="modal-fade">
                <div class="modal-backdrop">
                    <div class="modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
                        <div>
                            <button type="button" class="btn-close topright" @click="closeModal(false)" aria-label="Close modal">x</button>
                        </div>
                        <header class="modal-header" id="modalTitle">
                            <div>
                                <h4>#{{cardInfo.number}} - {{cardInfo.title}}</h4>
                            </div>
                        </header>
                        <div v-if="loading">
                            <section class="model-body" id="modalDescription">
                                <VueLoading></VueLoading>
                            </section>
                        </div>
                        <div v-if="!loading">
                            <section class="modal-body" id="modalDescription">
                                <label for="cardTitle">Title:</label>
                                <input type="text" id="cardTitle" v-model="cardInfo.title" />
                                <label for="assigneName">Assigned To:</label>
                                <input type="text" v-if="cardInfo.assignee != undefined" id="assigneName" :value="cardInfo.assignee.login" disabled />
                                <input type="text" v-if="cardInfo.assignee == undefined" id="assigneName" value="Unassigned" disabled />
                                <label for="dateCreated">Date Created:</label>
                                <input type="text" id="dateCreated" :value="getDate(cardInfo.created_at)" disabled />
                                <hr />
                                <label for="description">Description:</label>
                                <textarea :id="cardInfo.node_id" v-if="resizeTextarea(cardInfo.node_id)" v-model="cardInfo.body"></textarea>
                                <div v-if="cardInfo.comments != 0">
                                    <hr />
                                    <label>Comments:</label>
                                    <KanbanComments :commentUrl="cardInfo.comments_url"></KanbanComments>
                                </div>
                            </section>
                        </div>
                        <section class="modal-footer" id="modalFooter">
                            <div>
                                <slot name="footer">
                                    <button type="button" class="btn-button approve" v-if="!loading" @click="updateCard">
                                        Update
                                    </button>
                                    <button type="button" class="btn-button" @click="viewCard">
                                        View
                                    </button>
                                    <button type="button" class="btn-button" @click="closeModal(false)">
                                        Close
                                    </button>
                                </slot>
                            </div>
                        </section>
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
    import KanbanComments from '../KanBan/KanbanComments';
    import VueLoading from '../VueLoading';
    export default {
        name: "KanbanCard",
        props: {
            contentUrl: {
                type: String,
                required: true
            }
        },
        components: {
            KanbanComments,
            VueLoading
        },
        data() {
            return {
                cardInfo: [],
                showMore: false,
                loading: false
            }
        },
        mounted: function () {
            this.getCardInfo();
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
            getDate(date) {
                let elDate = new Date(date)
                return (elDate.getMonth() + 1) + '-'
                    + elDate.getDate() + '-'
                    + elDate.getFullYear()
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

<style scoped>
    label {
        color: white;
    }

    .cardText {
        color: white;
    }
</style>