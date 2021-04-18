<template>
    <div id="ManageServer">
        <div v-if="hasExistingSever">
            <vue-button @click="addServer">Add Channel</vue-button>

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

    export default {
        name: "ManageServer",
        components: {
            Form,
            HelpDocumentation,
            'vue-select': fieldSelect,
            'vue-button': fieldButton
        },
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
        beforeRouteEnter(to, from, next) {
            next((vm) => {
                vm.prevRoute = from
            })
        },
        mounted: function () {
            this.getServers();
        },
        created: function () {
            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
            else {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin && !this.$store.getters.isClientAdmin) {
                    this.$router.push('/unauthorized')
                }
            }
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
                    this.$message("Error loading account servers");
                })
            },
            reloadAuthentication() {
                this.$store.dispatch('loadRoles');
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
                this.$message("Successfully updated!");
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