<template>
    <div id="GitHub">
        <div if="loaded">
            <h1>{{project.name}}</h1>
        </div>
        <div class="lists">
            <div v-for="column in columns" class="list">
                <header>{{column.name}}</header>
                <KanbanColumn :columnId="column.id"></KanbanColumn>
                <footer><a href="https://github.com/The1CABAL/SkaldBot/projects/1" target="_blank" style="text-decoration: none; color: black;">View Board</a></footer>
            </div>
        </div>
    </div>
</template>

<script>
    import KanbanColumn from '../../components/KanBan/KanbanColumn';
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
        mounted: function () {
            this.loadProject();
        },
        methods: {
            async loadProject() {
                await this.$store.dispatch('getProjects').then(() => {
                    this.project = this.$store.getters.getProjects;
                }).catch(() => {
                    this.$message("Error getting github project")
                });

                if (this.project != undefined) {
                    var projectId = this.project.id;

                    await this.$store.dispatch('getProjectColumns', projectId).then(() => {
                        this.columns = this.$store.getters.getProjectColumns;
                    }).catch(() => {
                        this.$message("Error getting project columns")
                    })
                }
                else {
                    this.loaded = true;
                    this.msg = "Error getting data";
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
            background-color: #e2e4e6;
            color: #333;
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