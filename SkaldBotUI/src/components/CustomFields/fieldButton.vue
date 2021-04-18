<template>
    <button :class="fieldClasses"
            @click="onClick"
            :id="id"
            :type="type">
        <slot></slot>
    </button>
</template>

<script>
    export default {
        name: "Button",

        props: {
            id: {
                type: String,
                required: false
            },
            varient: {
                type: String,
                default: 'primary'
            },
            type: {
                type: String,
                default: 'button'
            }
        },

        methods: {
            onClick() {
                this.$emit('click');
            }
        },

        computed: {
            fieldClasses() {
                let baseButtonClass = 'min-w-32 max-w-xs w-auto pr-2 pl-2 mb-2 h-8 rounded-md'

                if (this.varient.toLowerCase() === 'secondary') {
                    return `${baseButtonClass} bg-hover hover:bg-secondary`
                }

                if (this.varient.toLowerCase() === 'danger') {
                    return `${baseButtonClass} bg-red-500 hover:bg-red-300`
                }

                if (this.varient.toLowerCase() === 'close') {
                    return `justify-end text-right pr-4`
                }

                return `${baseButtonClass} bg-secondary hover:bg-hover`
            }
        }
    }
</script>