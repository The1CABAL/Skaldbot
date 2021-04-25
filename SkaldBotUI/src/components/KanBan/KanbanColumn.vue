<template>
    <div id="column" class="kanban">
        <ul>
            <li v-for="card in cards" :key="card.id">
                <div>
                    <KanbanCard :contentUrl="card.content_url" @ReloadGithub="reloadGithub"></KanbanCard>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
    import KanbanCard from '../KanBan/KanbanCard';
    export default {
        name: "KanbanColumn",
        components: {
            KanbanCard
        },
        props: {
            columnId: {
                type: Number,
                required: true
            }
        },
        data() {
            return {
                cards: []
            }
        },
        mounted: function () {
            this.getCards();
        },
        methods: {
            async getCards() {
                var colId = this.columnId;
                await this.$store.dispatch('getProjectCardsByColumn', colId).then(() => {
                    this.cards = this.$store.getters.getColumnCards;
                }).catch(() => {
                    this.error("Error loading cards for column id" + colId);
                })
            },
            reloadGithub(value) {
                this.$emit('ReloadGithubPage', value);
            }
        }
    }
</script>

<style scoped>
    .kanban ul {
        list-style: none;
        margin: 0;
        max-height: 600px;
        overflow: auto;
        padding-left: 0px;
    }

        .kanban ul li {
            background-color: #fff;
            padding: 10px;
            border-radius: 3px;
            box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
        }

            .kanban ul li:not(:last-child) {
                margin-bottom: 10px;
            }
</style>