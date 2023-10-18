<template>
<div v-if="isOpen" class="modal">
    <div class="modal-background"></div>
    <div class="modal-content">
        <p>{{ message }}</p>
        <br />
        <div class="modal-buttons ">
            <button class="mr-3" @click="confirm">
                <inline-svg :class="['h-full', 'align-middle', 'w-7', 'modal-button-continue']"
                            :src="require('@/assets/icons/check.svg')">
                </inline-svg>
            </button> &nbsp;&nbsp;
            <button @click="cancel">
                <inline-svg :class="['h-full', 'align-middle', 'w-4']"
                            :src="require('@/assets/icons/close.svg')">
                </inline-svg>
            </button>
        </div>
    </div>
</div>
</template>

<script>
export default {
    props: ['isOpen', 'message'],
    methods: {
        confirm() {
            this.$emit('confirmed');
        },
        cancel() {
            this.$emit('canceled');
        },
    },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
}

.modal-button-continue {
    text-color: #d2725b;
}

</style>
