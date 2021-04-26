<template>
    <div id="column">
        <ul class="list-none m-0 overflow-auto pl-0 text-white space-y-3 size">
            <li class="bg-primary p-3 rounded-lg shadow-sm" v-for="card in cards" :key="card.id">
                <KanbanCard :contentUrl="card.content_url" @ReloadGithub="reloadGithub"></KanbanCard>
            </li>
        </ul>
        <div v-if="noCards" class="bg-primary p-3 rounded-lg shadow-sm">
            <p>No Issues</p>
        </div>
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

        computed: {
            noCards() {
                return this.cards.length <= 0;
            }
        },

        data() {
            return {
                cards: []
            }
        },

        mounted() {
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
    .size{
        max-height: 740px;
    }
</style>