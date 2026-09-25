<template>
    <tr :class="{ mine: isMe }">
        <td class="col-rank">
            <span :class="['rank-badge', medalClass, { me: isMe }]">
                {{ user.leaderboard_rank }}
            </span>
        </td>
        <td class="col-user">
            {{ user._id }}
            <span class="you-pill" v-if="isMe">You</span>
        </td>
        <td class="col-score">
            <div class="score">
                <span class="score-number">{{ user.percentage }}%</span>
                <span class="score-track">
                    <span class="score-fill" :style="{ width: user.percentage + '%' }"></span>
                </span>
            </div>
        </td>
        <td class="col-time">{{ formattedTime }}</td>
    </tr>
</template>


<script>
import { computed } from 'vue';

    export default {
        props: ['user', "isMe"],
        // TODO: medalClass, formattedTime — see chat message below
        setup(props) {
            const medalClass = computed(() => {
                return props.user.leaderboard_rank == 1 ?
                    'gold' : props.user.leaderboard_rank == 2 ?
                        'silver' : props.user.leaderboard_rank == 3 ?
                            'bronze' : ''
            })

            const formattedTime = computed(() => {
                if (props.user.time_taken == null) return '-'

                const total = Math.round(Number(props.user.time_taken))
                const h = Math.floor(total / 3600)
                const m = Math.floor((total % 3600) / 60)
                const s = total % 60

                if (h > 0) return `${h}h ${String(m).padStart(2, '0')}m ${String(s).padStart(2, '0')}s`
                if (m > 0) return `${m}m ${String(s).padStart(2, '0')}s`
                return `${s}s`
            })

            return { medalClass, formattedTime }
        }
    }
</script>

<style scoped>
tr {
  border-bottom: 1px solid #edf2f7;
}
tr:last-child {
  border-bottom: none;
}
tr.mine {
  background: #ebf4ff;
}
tr.mine td:first-child {
  box-shadow: inset 4px 0 0 #2b6cb0;
}
 
td {
  padding: 12px;
  color: #1a202c;
  vertical-align: middle;
  font-family: 'Inter', sans-serif;
}
.col-user { font-weight: 600; }
.col-time {
  font-variant-numeric: tabular-nums;
  color: #4a5568;
}
 
/* Rank badge */
.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  height: 34px;
  border-radius: 50%;
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
  color: #4a5568;
  background: #edf2f7;
}
.rank-badge.gold { background: #f6e05e; color: #744210; }
.rank-badge.silver { background: #e2e8f0; color: #2d3748; }
.rank-badge.bronze { background: #f6ad55; color: #7b341e; }
.rank-badge.me { box-shadow: 0 0 0 2px #2b6cb0; }
 
.you-pill {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 8px;
  border-radius: 999px;
  background: #2b6cb0;
  color: #ffffff;
  font-size: 0.75rem;
  font-weight: 600;
  vertical-align: middle;
}
 
/* Score */
.score {
  display: flex;
  align-items: center;
  gap: 10px;
}
.score-number {
  min-width: 52px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
.score-track {
  flex: 1;
  height: 8px;
  border-radius: 999px;
  background: #edf2f7;
  overflow: hidden;
}
.score-fill {
  display: block;
  height: 100%;
  border-radius: 999px;
  background: #38a169;
}
 
@media (max-width: 640px) {
  .score-track { display: none; }
}
</style>