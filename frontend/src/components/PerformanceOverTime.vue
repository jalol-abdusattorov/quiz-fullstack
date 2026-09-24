<template>
  <section class="performance" v-if="attempts.length">
    <h2 class="title">Performance Over Time</h2>

    <!-- Summary -->
    <div class="summary">
      <div class="summary-item">
        <span class="summary-value">{{ fmt(latest.percentage) }}%</span>
        <span class="summary-label">Latest score</span>
      </div>
      <div class="summary-item">
        <span class="summary-value" :class="trendClass(overallChange)">
          {{ signed(overallChange) }}
        </span>
        <span class="summary-label">Since first quiz</span>
      </div>
      <div class="summary-item">
        <span class="summary-value">{{ improvedCount }} of {{ comparable }}</span>
        <span class="summary-label">Quizzes beat the previous one</span>
      </div>
    </div>

    <!-- Chart -->
    <div class="chart-wrap">
      <svg
        class="chart"
        :viewBox="`0 0 ${W} ${H}`"
        role="img"
        :aria-label="`Line chart of your score across ${attempts.length} quizzes`"
        @mouseleave="active = null"
      >
        <defs>
          <linearGradient id="perf-area" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#2b6cb0" stop-opacity="0.22" />
            <stop offset="100%" stop-color="#2b6cb0" stop-opacity="0" />
          </linearGradient>
        </defs>

        <!-- Grid + Y labels -->
        <g v-for="tick in [0, 25, 50, 75, 100]" :key="tick">
          <line
            :x1="PAD.left"
            :x2="W - PAD.right"
            :y1="y(tick)"
            :y2="y(tick)"
            class="grid"
          />
          <text :x="PAD.left - 10" :y="y(tick) + 4" class="axis-label" text-anchor="end">
            {{ tick }}%
          </text>
        </g>

        <!-- Area + line -->
        <path :d="areaPath" fill="url(#perf-area)" />
        <path :d="linePath" class="line" />

        <!-- Hover guide -->
        <line
          v-if="active !== null"
          :x1="points[active].x"
          :x2="points[active].x"
          :y1="PAD.top"
          :y2="H - PAD.bottom"
          class="guide"
        />

        <!-- X labels (first, last, and every few in between) -->
        <text
          v-for="(p, i) in points"
          v-show="showXLabel(i)"
          :key="'x' + i"
          :x="p.x"
          :y="H - 8"
          class="axis-label"
          text-anchor="middle"
        >
          {{ i + 1 }}
        </text>

        <!-- Points -->
        <g v-for="(p, i) in points" :key="p.id">
          <circle
            :cx="p.x"
            :cy="p.y"
            :r="active === i ? 7 : 5"
            :class="['dot', trendClass(p.change)]"
          />
          <!-- Larger invisible target for hover / keyboard -->
          <circle
            :cx="p.x"
            :cy="p.y"
            r="16"
            fill="transparent"
            tabindex="0"
            :aria-label="pointLabel(p, i)"
            @mouseenter="active = i"
            @focus="active = i"
            @blur="active = null"
          />
        </g>
      </svg>

      <!-- Tooltip -->
      <div
        v-if="active !== null"
        class="tooltip"
        :style="tooltipStyle"
      >
        <div class="tooltip-title">Quiz {{ active + 1 }}</div>
        <div class="tooltip-score">{{ fmt(points[active].percentage) }}%</div>
        <div
          v-if="points[active].change !== null"
          :class="['tooltip-change', trendClass(points[active].change)]"
        >
          {{ signed(points[active].change) }} vs previous
        </div>
        <div v-else class="tooltip-change muted">First quiz</div>
      </div>
    </div>

    <p class="x-caption">Quiz number, oldest to newest</p>

    <!-- Change per quiz -->
    <div class="changes">
      <h3 class="changes-title">Change from the previous quiz</h3>
      <div class="changes-bars" role="list">
        <div
          v-for="(p, i) in points"
          :key="'c' + p.id"
          class="change-col"
          role="listitem"
          :title="pointLabel(p, i)"
          @mouseenter="active = i"
          @mouseleave="active = null"
        >
          <div class="change-half top">
            <div
              v-if="p.change !== null && p.change > 0"
              class="change-bar up"
              :style="{ height: barHeight(p.change) }"
            ></div>
          </div>
          <div class="change-half bottom">
            <div
              v-if="p.change !== null && p.change < 0"
              class="change-bar down"
              :style="{ height: barHeight(p.change) }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="performance empty" v-else>
    <h2 class="title">Performance Over Time</h2>
    <p>Finish a quiz to start tracking your progress.</p>
  </section>
</template>

<script>
import { computed, ref } from 'vue'

export default {
  name: 'PerformanceOverTime',
  props: {
    // Array from your API: [{ _id, percentage, previous_percentage, percentage_growth }]
    data: { type: Array, default: () => [] }
  },
  setup(props) {
    const W = 640
    const H = 300
    const PAD = { top: 20, right: 24, bottom: 34, left: 48 }
    const active = ref(null)

    const attempts = computed(() => (Array.isArray(props.data) ? props.data : []))

    const points = computed(() => {
      const n = attempts.value.length
      const innerW = W - PAD.left - PAD.right
      return attempts.value.map((a, i) => ({
        id: a._id,
        percentage: a.percentage,
        // Change in percentage points (e.g. 20% -> 66.7% = +46.7),
        // easier to read than the relative growth value (+233%)
        change: a.previous_percentage === null || a.previous_percentage === undefined
          ? null
          : a.percentage - a.previous_percentage,
        x: n === 1 ? PAD.left + innerW / 2 : PAD.left + (innerW / (n - 1)) * i,
        y: y(a.percentage)
      }))
    })

    function y(value) {
      const innerH = H - PAD.top - PAD.bottom
      return PAD.top + innerH - (value / 100) * innerH
    }

    const linePath = computed(() =>
      points.value.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ')
    )

    const areaPath = computed(() => {
      if (!points.value.length) return ''
      const first = points.value[0]
      const last = points.value[points.value.length - 1]
      const base = H - PAD.bottom
      return `${linePath.value} L${last.x},${base} L${first.x},${base} Z`
    })

    const latest = computed(() => attempts.value[attempts.value.length - 1] || {})
    const overallChange = computed(() =>
      attempts.value.length > 1
        ? latest.value.percentage - attempts.value[0].percentage
        : null
    )
    const comparable = computed(() => points.value.filter(p => p.change !== null).length)
    const improvedCount = computed(() => points.value.filter(p => p.change > 0).length)

    const maxChange = computed(() =>
      Math.max(10, ...points.value.map(p => Math.abs(p.change || 0)))
    )
    const barHeight = change => `${(Math.abs(change) / maxChange.value) * 100}%`

    const fmt = v => (Math.round(v * 10) / 10).toString()
    const signed = v => {
      if (v === null || v === undefined) return '—'
      const r = Math.round(v * 10) / 10
      return `${r > 0 ? '+' : ''}${r} pts`
    }
    const trendClass = v => {
      if (v === null || v === undefined || Math.abs(v) < 0.05) return 'flat'
      return v > 0 ? 'up' : 'down'
    }
    const pointLabel = (p, i) =>
      `Quiz ${i + 1}: ${fmt(p.percentage)}%` +
      (p.change === null ? ', first quiz' : `, ${signed(p.change)} vs previous`)

    const showXLabel = i => {
      const n = points.value.length
      if (n <= 10) return true
      return i === 0 || i === n - 1 || (i + 1) % 5 === 0
    }

    const tooltipStyle = computed(() => {
      if (active.value === null) return {}
      const p = points.value[active.value]
      const left = Math.min(Math.max((p.x / W) * 100, 12), 88)
      return { left: `${left}%`, top: `${(p.y / H) * 100}%` }
    })

    return {
      W, H, PAD, active, attempts, points, linePath, areaPath, latest,
      overallChange, comparable, improvedCount, barHeight, tooltipStyle,
      y, fmt, signed, trendClass, pointLabel, showXLabel
    }
  }
}
</script>

<style scoped>
.performance {
  background: #ffffff;
  border-radius: 16px;
  padding: 32px;
  max-width: 800px;
  margin: 24px auto 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  font-family: 'Inter', sans-serif;
}

.performance.empty {
  text-align: center;
  color: #718096;
}

.title {
  font-family: 'Poppins', 'Inter', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 24px;
  text-align: center;
}

/* Summary */
.summary {
  display: flex;
  justify-content: space-around;
  gap: 16px;
  margin-bottom: 24px;
  text-align: center;
}
.summary-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.summary-value {
  font-family: 'Poppins', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a365d;
  line-height: 1.1;
}
.summary-label {
  font-size: 0.85rem;
  color: #718096;
}

/* Chart */
.chart-wrap {
  position: relative;
}
.chart {
  width: 100%;
  height: auto;
  display: block;
  overflow: visible;
}
.grid {
  stroke: #e7e4e4;
  stroke-width: 1;
}
.axis-label {
  font-size: 11px;
  fill: #718096;
  font-family: 'Inter', sans-serif;
}
.line {
  fill: none;
  stroke: #2b6cb0;
  stroke-width: 2.5;
  stroke-linejoin: round;
  stroke-linecap: round;
}
.guide {
  stroke: #a0aec0;
  stroke-width: 1;
  stroke-dasharray: 4 4;
}
.dot {
  stroke: #ffffff;
  stroke-width: 2;
  transition: r 0.15s ease;
}
.dot.up { fill: #38a169; }
.dot.down { fill: #dd3620; }
.dot.flat { fill: #2b6cb0; }

circle:focus-visible {
  outline: 2px solid #2b6cb0;
  outline-offset: 2px;
}

.x-caption {
  text-align: center;
  font-size: 0.8rem;
  color: #718096;
  margin: 4px 0 0;
}

/* Tooltip */
.tooltip {
  position: absolute;
  transform: translate(-50%, calc(-100% - 16px));
  background: #1a202c;
  color: #ffffff;
  border-radius: 10px;
  padding: 8px 12px;
  text-align: center;
  pointer-events: none;
  white-space: nowrap;
  z-index: 2;
}
.tooltip-title {
  font-size: 0.75rem;
  color: #cbd5e0;
}
.tooltip-score {
  font-family: 'Poppins', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
}
.tooltip-change {
  font-size: 0.8rem;
  font-weight: 600;
}
.tooltip-change.up { color: #68d391; }
.tooltip-change.down { color: #fc8181; }
.tooltip-change.flat,
.tooltip-change.muted { color: #cbd5e0; }

/* Change bars */
.changes {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid #e7e4e4;
}
.changes-title {
  font-family: 'Poppins', 'Inter', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 12px;
  text-align: center;
}
.changes-bars {
  display: flex;
  gap: 6px;
  height: 120px;
}
.change-col {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.change-half {
  flex: 1;
  display: flex;
}
.change-half.top { align-items: flex-end; border-bottom: 1px solid #cbd5e0; }
.change-half.bottom { align-items: flex-start; }
.change-bar {
  width: 100%;
  min-height: 2px;
}
.change-bar.up { background: #38a169; border-radius: 4px 4px 0 0; }
.change-bar.down { background: #dd3620; border-radius: 0 0 4px 4px; }

/* Text trend colors */
.summary-value.up { color: #2f855a; }
.summary-value.down { color: #b52e1c; }

@media (max-width: 640px) {
  .performance { padding: 20px 16px; }
  .summary { flex-direction: column; }
}

@media (prefers-reduced-motion: reduce) {
  .dot { transition: none; }
}
</style>