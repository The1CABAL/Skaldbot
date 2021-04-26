<template>
    <div id="GitHub" class="h-full overflow-x-auto">
        <div if="loaded">
            <h1 class="font-bold tracking-wide mb-5 border-b-2 border-hoverLight">{{project.name}}</h1>
        </div>
        <div class="lists">
            <div v-for="column in columns" class="list text-white bg-primaryLight rounded-md" :key="column.id">
                <header class="border-b-2 border-secondary">{{column.name}}</header>
                <KanbanColumn class="mb-3" :columnId="column.id" @ReloadGithubPage="reloadPage"></KanbanColumn>
                <footer class="border-t-2 border-secondary pt-1"><a href="https://github.com/The1CABAL/SkaldBot/projects/1" target="_blank" style="text-decoration: none">View Board</a></footer>
            </div>
        </div>
    </div>
</template>

<script>
    import KanbanColumn from '../../components/KanBan/KanbanColumn';
    import PageMixin from '@/mixins/page-mixin'
    export default {
        name: "GitHub",

        components: {
            KanbanColumn
        },

        data() {
            return {
                loaded: false,
                project: [],
                columns: [],
                cards: [],
                msg: ''
            }
        },

        mixins: [PageMixin],

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                this.loadProject();
                this.pageReady();
            })
        },

        methods: {
            async loadProject() {
                await this.$store.dispatch('getProjects').then(() => {
                    this.project = this.$store.getters.getProjects;
                }).catch(() => {
                    this.error("Error getting github project")
                });

                if (this.project != undefined) {
                    var projectId = this.project.id;

                    await this.$store.dispatch('getProjectColumns', projectId).then(() => {
                        this.columns = this.$store.getters.getProjectColumns;
                    }).catch(() => {
                        this.error("Error getting project columns")
                    })
                }
                else {
                    this.loaded = true;
                    this.msg = "Error getting data";
                }
            },

            async reloadPage(value) {
                if (value == "Reload") {
                    this.loaded = false;
                    this.project = [];
                    this.columns = [];
                    this.cards = [];

                    await this.loadProject();
                }
            }
        }
    }
</script>

<style>
    .lists {
        display: flex;
        overflow-x: auto;
    }

        .lists > * {
            flex: 0 0 auto;
            margin-left: 10px;
        }

        .lists::after {
            content: '';
            flex: 0 0 10px;
        }

    .list {
        width: 300px;
        height: calc(100% - 10px - 17px);
    }

        .list > * {
            padding: 0 10px;
        }

        .list header {
            line-height: 36px;
            font-size: 16px;
            font-weight: bold;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }

        .list footer {
            line-height: 36px;
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
        }
</style>