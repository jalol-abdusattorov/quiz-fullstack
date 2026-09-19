<template>
    <div class="backdrop" @click.self="closeModal">
        <div class="modal">
            <slot>
                <h1>No Content Yet</h1>
                <p>...</p>
            </slot>
        </div>
    </div>
</template>

<script>
    export default {
        emits: ['close'],
        setup(props, { emit }) {
            const closeModal = () => {
                emit('close')
            }

            return { closeModal }
        }
    }
</script>

<style scoped>
.modal {
    width: 600px;
    padding: 20px;
    margin: 250px auto;
    background: white;
    border-radius: 10px;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.backdrop {
    top: 0;
    position: fixed;
    background: rgba(0, 0, 0, 0.5);
    width: 100%;
    height: 100%;
}

</style>