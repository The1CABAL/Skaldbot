<template>
    <div class="flex flex-col flex-grow border-r border-gray-200 pb-4 bg-primary overflow-y-auto">
        <div class="mt-5 flex-grow flex flex-col">
            <nav class="flex-1 bg-primary space-y-3" aria-label="Sidebar">
                <nav-link to="/dashboardhome" sideNavLink @click="sideNavClick">Dashboard Home</nav-link>
                <nav-link to="/manageusers" sideNavLink @click="sideNavClick">Users</nav-link>
                <nav-link to="/pendingitems" sideNavLink @click="sideNavClick">Pending Items</nav-link>
                <nav-link to="/managedocumentation" sideNavLink @click="sideNavClick">Manage Help</nav-link>
                <nav-link to="/manageforms" sideNavLink @click="sideNavClick">Manage Forms</nav-link>
                <nav-link to="/managestories" sideNavLink @click="sideNavClick">Manage Stories</nav-link>
                <nav-link to="/managewisdoms" sideNavLink @click="sideNavClick">Manage Wisdoms</nav-link>
                <nav-link to="/github" sideNavLink @click="sideNavClick">GitHub Project</nav-link>
            </nav>
        </div>
    </div>
</template>

<script>
    import navLink from '@/components/Nav/navLink';

    export default {
        name: "SidebarNav",

        components: {
            'nav-link': navLink
        },

        methods: {
            sideNavClick() {
                console.log("huh");
                this.$emit('sideNavClick');
            }
        }
    }
</script>