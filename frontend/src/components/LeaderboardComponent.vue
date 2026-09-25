<template>
        <div class="container">
        <div class="table-wrap">
            <table class="table">
                <thead>
                    <tr>
                        <th class="col-rank">Rank</th>
                        <th>User</th>
                        <th class="col-score">Score</th>
                        <th class="col-time">Time</th>
                    </tr>
                </thead>
                <tbody>
                    <UserLeaderboard
                        v-for="user in leaderboard"
                        :key="user.id"
                        :user="user"
                        :is-me="user._id === currentUsername"
                    />
                </tbody>
            </table>
        </div>
    </div>
</template>


<script>
import UserLeaderboard from './UserLeaderboard.vue';

    export default {
        props: ['leaderboard', "currentUsername"],
        components: { UserLeaderboard }
    }
</script>

<style scoped>
.table-wrap {
  overflow-x: auto;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table :deep(th) {
  text-align: left;
  font-size: 0.85rem;
  font-weight: 600;
  color: #718096;
  padding: 10px 12px;
  border-bottom: 2px solid #e7e4e4;
}
 
.col-rank { width: 72px; }
.col-score { width: 220px; }
.col-time { width: 90px; }
 
@media (max-width: 640px) {
  .col-score { width: auto; }
}
</style>