<template>
    <div id="KanbanCard">
        <div v-if="!showMore" @click="enableMore">
            <p>#{{cardInfo.number}} - {{cardInfo.title}}</p>
        </div>
        <div v-if="showMore">
            <transition name="modal-fade">
                <div class="modal-backdrop">
                    <div class="modal" role="dialog" aria-labelledby="modalTitle" aria-describedby="modalDescription">
                        <div>
                            <button type="button" class="btn-close topright" @click="closeModal" aria-label="Close modal">x</button>
                        </div>
                        <header class="modal-header" id="modalTitle">
                            <div>
                                <h4>#{{cardInfo.number}} - {{cardInfo.title}}</h4>
                            </div>
                        </header>
                        <section class="modal-body" id="modalDescription">
                            <label for="assigneName">Assigned To:</label>
                            <input type="text" v-if="cardInfo.assignee != undefined" id="assigneName" :value="cardInfo.assignee.login" disabled />
                            <input type="text" v-if="cardInfo.assignee == undefined" id="assigneName" value="Unassigned" disabled/>
                            <label for="dateCreated">Date Created:</label>
                            <input type="text" id="dateCreated" :value="getDate(cardInfo.created_at)" disabled />
                            <hr />
                            <label for="description">Description:</label>
                            <textarea :id="cardInfo.node_id" v-if="resizeTextarea(cardInfo.node_id)" v-model="cardInfo.body" disabled></textarea>
                            <div v-if="cardInfo.comments != 0">
                                <hr />
                                <label>Comments:</label>
                                <KanbanComments :commentUrl="cardInfo.comments_url"></KanbanComments>
                            </div>
                        </section>
                        <section class="modal-footer" id="modalFooter">
                            <div>
                                <slot name="footer">
                                    <button type="button" class="btn-button approve" @click="viewCard">
                                        View
                                    </button>
                                    <button type="button" class="btn-button" @click="closeModal">
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
    export default {
        name: "KanbanCard",
        props: {
            contentUrl: {
                type: String,
                required: true
            }
        },
        components: {
            KanbanComments
        },
        data() {
            return {
                cardInfo: [],
                showMore: false
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
                    this.$message("Error getting card info for card id " + id);
                })
            },
            enableMore() {
                this.showMore = true;
            },
            closeModal() {
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
    label{
        color: white;
    }

    .cardText{
        color: white;
    }
</style>