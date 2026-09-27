<template>
    <div>
        <div class="empty-user-stats">
            <div class="empty-icon">
                📊
            </div>

            <h1>You currently have no statistics</h1>

            <p>
                Complete some quizzes to start building your statistics
                and see your performance here.
            </p>

            <router-link
                class="router-link-to-quizzes"
                :to="{ name: 'Quizzes' }"
            >
                Browse Quizzes
                <span>→</span>
            </router-link>
        </div>
    </div>
</template>

<script>
    export default {
        
    }
</script>

<style scoped>
/* =========================================================
   Main Quiz Link
========================================================= */

.router-link-to-quizzes {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    padding: 10px 17px;

    border-radius: 9px;

    background: #2563eb;
    color: #ffffff;

    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    font-weight: 600;

    text-decoration: none;

    transition:
        background 0.18s ease,
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

.router-link-to-quizzes span {
    font-size: 1.05rem;
    transition: transform 0.18s ease;
}

.router-link-to-quizzes:hover {
    background: #1d4ed8;
    transform: translateY(-1px);
    box-shadow: 0 5px 12px rgba(37, 99, 235, 0.2);
}

.router-link-to-quizzes:hover span {
    transform: translateX(3px);
}

/* =========================================================
   Empty Statistics
========================================================= */

.empty-user-stats {
    width: min(560px, 100%);
    margin: 80px auto 0;
    padding: 42px 36px;

    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;

    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;

    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
    box-sizing: border-box;
}

.empty-icon {
    width: 68px;
    height: 68px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin-bottom: 20px;

    background: #eff6ff;
    border: 1px solid #dbeafe;
    border-radius: 16px;

    font-size: 30px;
}

.empty-user-stats h1 {
    margin: 0 0 10px;

    font-family: 'Poppins', 'Inter', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;

    color: #0f172a;
}

.empty-user-stats p {
    max-width: 430px;

    margin: 0 0 24px;

    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    line-height: 1.6;

    color: #64748b;
}
</style>