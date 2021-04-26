<template>
    <div id="ManageServer">
        <div v-if="hasExistingSever">
            <div class="flex flex-1 w-full space-x-2">
                <vue-button @click="goBack">Go Back</vue-button>
                <vue-button @click="addServer">Add Channel</vue-button>
            </div>

            <vue-select :items="servers" name-key="Nickname" value-key="Id" @change="selectServer" class="pb-2"/>

            <div v-if="serverLoaded && !newServer">
                <Form :formKey="formKey" :passedModel="selectedServer" @ServerSuccess="setSuccess" />
            </div>
            <div v-if="newServer">
                <Form :formKey="formKey" :passedModel="selectedServer" @ServerSuccess="setSuccess" />
            </div>
        </div>
        <div v-if="!hasExistingSever">
            <p>Add new server</p>
            <Form :formKey="formKey" :passedModel="selectedServer" @ServerSuccess="setSuccess" />
        </div>
        <hr />
        <vue-button @click="openHelp" varient="secondary" class="mt-2">Help</vue-button>
        <HelpDocumentation v-if="showHelp" :HelpContentKey="helpContentKey" @close="closeHelp"></HelpDocumentation>
    </div>
</template>

<script>
    import Form from '../../components/Forms/Form';
    import HelpDocumentation from '../../components/HelpDocumentation'
    import fieldSelect from '../../components/CustomFields/fieldSelect';
    import fieldButton from '../../components/CustomFields/fieldButton';
    import PageMixin from '@/mixins/page-mixin.js'

    export default {
        name: "ManageServer",

        components: {
            Form,
            HelpDocumentation,
            'vue-select': fieldSelect,
            'vue-button': fieldButton
        },

        mixins: [PageMixin],

        data() {
            return {
                formKey: 'ManageServer',
                hasExistingSever: false,
                serverLoaded: false,
                newServer: false,
                showHelp: false,
                helpContentKey: 'AddServerHelp',
                prevRoute: {},
                servers: [],
                selectedServer: []
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.masterAdmin && !this.admin && !this.clientAdmin) {
                    this.$router.push('/unauthorized')
                }

                this.getServers();
                this.pageReady();
            })
        },

        methods: {
            getServers() {
                this.newServer = false;
                this.selectedServer = [];
                this.servers = [];
                this.serverLoaded = false;
                var accountId = this.$store.getters.getAccountId;
                this.$store.dispatch('getAccountServers', accountId).then(() => {
                    this.servers = this.$store.getters.getServers;
                    if (this.servers.length > 0) {
                        this.hasExistingSever = true;
                    }
                    else {
                        this.addServer();
                    }
                }).catch(err => {
                    console.log(err);
                    this.error("Error loading account servers");
                })
            },

            addServer() {
                var defaultModel = {
                    Id: 0,
                    ServerId: "",
                    AccountId: this.$store.getters.getAccountId,
                    DailyWisdom: true,
                    WeeklyStory: true,
                    UpdateDate: ""
                }
                var model = [defaultModel]
                this.selectedServer = model;
                this.newServer = true;
                if (this.servers.length > 0) {
                    var element = document.getElementById("serverSelect");
                    element.selectedIndex = 0;
                }
                event.preventDefault;
            },

            selectServer(e) {
                this.newServer = false

                if (!e) {
                    this.selectedServer = [];
                    this.serverLoaded = false;
                    return;
                }

                const serverId = e['Id'];

                if (serverId != "Select") {
                    this.$store.dispatch('getServerById', serverId).then(() => {
                        this.selectedServer = { ...this.$store.getters.getServer };
                        this.serverLoaded = true;
                    })
                }
            },

            openHelp() {
                this.showHelp = true;
            },

            closeHelp() {
                this.showHelp = false;
            },

            setSuccess() {
                this.success("Successfully updated!");
                this.getServers();
            }
        }
    }
</script>

<style scoped>
    .buttonSection {
        display: inline-flex;
    }
</style>