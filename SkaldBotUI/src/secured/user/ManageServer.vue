<template>
    <div id="ManageServer">
        <div v-if="hasExistingSever">
            <div class="buttonSection" @change="selectServer($event)">
                <button type="button" @click="addServer" class="btn-button">Add Server</button>
                <select class="select-css" id="serverSelect">
                    <option value="select">Select</option>
                    <option v-for="server in servers" :key="server.Id" :value="server.Id">{{server.Nickname}}</option>
                </select>
            </div>
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
        <button type="button" v-on:click="openHelp" class="btn-button">Help</button>
        <HelpDocumentation v-if="showHelp" :HelpContentKey="helpContentKey" @close="closeHelp"></HelpDocumentation>
    </div>
</template>

<script>
    import Form from '../../components/Forms/Form';
    import HelpDocumentation from '../../components/HelpDocumentation'
    export default {
        name: "ManageServer",
        components: {
            Form,
            HelpDocumentation
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
                    DailyWisdom: 1,
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
                const serverId = e.target.options[e.target.options.selectedIndex].value;

                this.newServer = false

                if (serverId != "select") {
                    this.$store.dispatch('getServerById', serverId).then(() => {
                        this.selectedServer = { ...this.$store.getters.getServer };
                        this.serverLoaded = true;
                    })
                }
                else {
                    this.selectedServer = [];
                    this.serverLoaded = false;
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