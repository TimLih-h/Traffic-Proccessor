const POLL_INTERVAL_MS = 1000;
const HISTORY_WINDOW_MS = 60 * 1000;
const PAGE_SIZE = 10;

const cumulativeKeys = [
  "total_packets",
  "total_bytes",
  "incoming_packets",
  "outgoing_packets",
  "incoming_bytes",
  "outgoing_bytes",
  "tcp_packets",
  "udp_packets",
  "icmp_packets",
  "other_packets",
];

const elements = {
  statusDiode: document.getElementById("status-diode"),
  viewTitle: document.getElementById("view-title"),
  lastUpdated: document.getElementById("last-updated"),
  dashboardView: document.getElementById("dashboard-view"),
  tableView: document.getElementById("table-view"),
  viewTabs: Array.from(document.querySelectorAll(".view-tab")),
  metricButtons: Array.from(document.querySelectorAll(".toggle-button")),
  incomingRateLabel: document.getElementById("incoming-rate-label"),
  outgoingRateLabel: document.getElementById("outgoing-rate-label"),
  incomingRate: document.getElementById("incoming-rate"),
  outgoingRate: document.getElementById("outgoing-rate"),
  incomingTotalLabel: document.getElementById("incoming-total-label"),
  outgoingTotalLabel: document.getElementById("outgoing-total-label"),
  incomingTotal: document.getElementById("incoming-total"),
  outgoingTotal: document.getElementById("outgoing-total"),
  chartTitle: document.getElementById("chart-title"),
  chart: document.getElementById("traffic-chart"),
  resetButton: document.getElementById("reset-button"),
  refreshButton: document.getElementById("refresh-button"),
  exportButton: document.getElementById("export-button"),
  talkersBody: document.getElementById("talkers-body"),
  tableSummary: document.getElementById("table-summary"),
  packetCounts: {
    tcp_packets: document.getElementById("tcp-packets"),
    udp_packets: document.getElementById("udp-packets"),
    icmp_packets: document.getElementById("icmp-packets"),
    other_packets: document.getElementById("other-packets"),
  },
};

const emptyStats = {
  timestamp: "",
  status: "offline",
  total_packets: 0,
  total_bytes: 0,
  incoming_packets: 0,
  outgoing_packets: 0,
  incoming_bytes: 0,
  outgoing_bytes: 0,
  packets_per_second: 0,
  bytes_per_second: 0,
  tcp_packets: 0,
  udp_packets: 0,
  icmp_packets: 0,
  other_packets: 0,
  incoming_packets_per_second: 0,
  outgoing_packets_per_second: 0,
  incoming_bytes_per_second: 0,
  outgoing_bytes_per_second: 0,
  _timeMs: Date.now(),
};

const state = {
  view: "dashboard",
  metric: "packets",
  stats: { ...emptyStats },
  rawStats: null,
  previousRaw: null,
  resetPending: false,
  history: [],
  talkers: [],
};

function getStatsEndpoint() {
  const params = new URLSearchParams(window.location.search);
  const configuredEndpoint = params.get("api");

  if (configuredEndpoint) {
    return configuredEndpoint;
  }

  const runsOutsideBackend =
    window.location.protocol === "file:" ||
    (["localhost", "127.0.0.1"].includes(window.location.hostname) &&
      window.location.port !== "8080");

  return runsOutsideBackend
    ? "http://localhost:8080/packets"
    : `${window.location.origin}/packets`;
}

const statsEndpoint = getStatsEndpoint();

function getResetEndpoint() {
  const params = new URLSearchParams(window.location.search);
  const configuredEndpoint = params.get("resetApi");

  if (configuredEndpoint) {
    return configuredEndpoint;
  }

  try {
    const url = new URL(statsEndpoint, window.location.href);
    url.pathname = url.pathname.replace(/\/packets\/?$/, "/reset");
    url.search = "";
    return url.toString();
  } catch {
    return `${window.location.origin}/reset`;
  }
}

const resetEndpoint = getResetEndpoint();

function toNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function positive(value) {
  return Math.max(0, toNumber(value));
}

function formatNumber(value, maximumFractionDigits = 0) {
  return toNumber(value).toLocaleString(undefined, {
    maximumFractionDigits,
  });
}

function formatBytes(value) {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let amount = Math.max(0, toNumber(value));
  let unitIndex = 0;

  while (amount >= 1024 && unitIndex < units.length - 1) {
    amount /= 1024;
    unitIndex += 1;
  }

  const digits = amount >= 100 || unitIndex === 0 ? 0 : amount >= 10 ? 1 : 2;
  return `${formatNumber(amount, digits)} ${units[unitIndex]}`;
}

function formatMetricRate(value) {
  return state.metric === "packets" ? formatNumber(Math.round(value)) : formatBytes(value);
}

function formatMetricTotal(value) {
  return state.metric === "packets" ? formatNumber(value) : formatBytes(value);
}

function getTimeMs(stats) {
  const parsed = Date.parse(stats.timestamp);
  return Number.isNaN(parsed) ? Date.now() : parsed;
}

function getReceiveTimeMs() {
  const previousTime = state.rawStats?._timeMs || 0;
  return Math.max(Date.now(), previousTime + 1);
}

function formatClock(value) {
  const date = value ? new Date(value) : null;

  if (!date || Number.isNaN(date.getTime())) {
    return "--:--:--";
  }

  return [date.getHours(), date.getMinutes(), date.getSeconds()]
    .map((part) => String(part).padStart(2, "0"))
    .join(":");
}

function normalizeStats(payload) {
  const source = payload && typeof payload === "object" ? payload : {};
  const stats = { ...emptyStats, ...source };

  stats.incoming_packets =
    source.incoming_packets ?? source.in_packets ?? source.input_packets ?? 0;
  stats.outgoing_packets =
    source.outgoing_packets ??
    source.outcoming_packets ??
    source.out_packets ??
    source.output_packets ??
    0;
  stats.incoming_bytes = source.incoming_bytes ?? source.in_bytes ?? source.input_bytes ?? 0;
  stats.outgoing_bytes =
    source.outgoing_bytes ??
    source.outcoming_bytes ??
    source.out_bytes ??
    source.output_bytes ??
    0;

  cumulativeKeys.forEach((key) => {
    stats[key] = positive(stats[key]);
  });

  const protocolPackets =
    stats.tcp_packets + stats.udp_packets + stats.icmp_packets + stats.other_packets;
  const directionPackets = stats.incoming_packets + stats.outgoing_packets;
  const directionBytes = stats.incoming_bytes + stats.outgoing_bytes;

  stats.total_packets = stats.total_packets || protocolPackets || directionPackets;
  stats.total_bytes = stats.total_bytes || directionBytes;

  stats.packets_per_second = positive(stats.packets_per_second);
  stats.bytes_per_second = positive(stats.bytes_per_second);
  stats.status = stats.status === "online" ? "online" : "offline";
  stats._timeMs = getReceiveTimeMs();

  return stats;
}

function calculateDirectionalRates(rawStats) {
  const previous = state.previousRaw;

  if (!previous) {
    return {
      incoming_packets_per_second: 0,
      outgoing_packets_per_second: 0,
      incoming_bytes_per_second: 0,
      outgoing_bytes_per_second: 0,
    };
  }

  const elapsedSeconds = Math.max((rawStats._timeMs - previous._timeMs) / 1000, 0.25);
  const rate = (current, before, integer = false) => {
    const value = Math.max(0, (positive(current) - positive(before)) / elapsedSeconds);
    return integer ? Math.round(value) : value;
  };

  return {
    incoming_packets_per_second: rate(rawStats.incoming_packets, previous.incoming_packets, true),
    outgoing_packets_per_second: rate(rawStats.outgoing_packets, previous.outgoing_packets, true),
    incoming_bytes_per_second: rate(rawStats.incoming_bytes, previous.incoming_bytes),
    outgoing_bytes_per_second: rate(rawStats.outgoing_bytes, previous.outgoing_bytes),
  };
}

function appendHistory(stats) {
  if (stats.status !== "online") {
    return;
  }

  state.history.push({
    timeMs: stats._timeMs,
    incomingPackets: Math.round(stats.incoming_packets_per_second),
    outgoingPackets: Math.round(stats.outgoing_packets_per_second),
    incomingBytes: stats.incoming_bytes_per_second,
    outgoingBytes: stats.outgoing_bytes_per_second,
  });

  const cutoff = stats._timeMs - HISTORY_WINDOW_MS;
  state.history = state.history
    .filter((point) => point.timeMs >= cutoff)
    .sort((left, right) => left.timeMs - right.timeMs);
}

function normalizePercent(value, total) {
  if (typeof value === "string" && value.includes("%")) {
    return value;
  }

  const number = positive(value);
  if (total > 0) {
    return `${Math.round((number / total) * 100)}%`;
  }

  return `${Math.round(number)}%`;
}

function normalizeProtocols(row) {
  const source = row.protocols || row.top_protocols || row.topProtocols;
  const rowPackets = positive(row.packets ?? row.total_packets ?? row.totalPackets ?? 0);

  if (Array.isArray(source)) {
    return source.slice(0, 4).map((item) => {
      if (typeof item === "string") {
        return item;
      }

      const name = item.name || item.protocol || item.type || "Other";
      const explicitPercent = item.percent ?? item.percentage ?? item.share;
      const count = item.count ?? item.packets ?? item.value ?? 0;
      return `${name} ${normalizePercent(explicitPercent ?? count, explicitPercent === undefined ? rowPackets : 100)}`;
    });
  }

  if (source && typeof source === "object") {
    const total = Object.values(source).reduce((sum, value) => sum + positive(value), 0) || rowPackets;

    return Object.entries(source)
      .sort(([, left], [, right]) => positive(right) - positive(left))
      .slice(0, 4)
      .map(([name, value]) => `${name} ${normalizePercent(value, total)}`);
  }

  const counts = [
    ["TCP", row.tcp_packets ?? row.tcp ?? 0],
    ["UDP", row.udp_packets ?? row.udp ?? 0],
    ["ICMP", row.icmp_packets ?? row.icmp ?? 0],
    ["Other", row.other_packets ?? row.other ?? 0],
  ];
  const total = counts.reduce((sum, [, value]) => sum + positive(value), 0);

  return counts
    .filter(([, value]) => positive(value) > 0)
    .map(([name, value]) => `${name} ${normalizePercent(value, total)}`)
    .slice(0, 4);
}

function normalizePorts(row) {
  const source = row.ports || row.top_ports || row.topPorts;
  const rowPackets = positive(row.packets ?? row.total_packets ?? row.totalPackets ?? 0);

  if (Array.isArray(source)) {
    return source.slice(0, 4).map((item) => {
      if (typeof item === "string" || typeof item === "number") {
        return String(item);
      }

      const port = item.port ?? item.number ?? item.name ?? "--";
      const explicitPercent = item.percent ?? item.percentage ?? item.share;
      const count = item.count ?? item.packets ?? item.value;
      const suffix =
        explicitPercent === undefined && count === undefined
          ? ""
          : `(${normalizePercent(explicitPercent ?? count, explicitPercent === undefined ? rowPackets : 100)})`;
      return `${port}${suffix}`;
    });
  }

  if (source && typeof source === "object") {
    const total = Object.values(source).reduce((sum, value) => sum + positive(value), 0) || rowPackets;

    return Object.entries(source)
      .sort(([, left], [, right]) => positive(right) - positive(left))
      .slice(0, 4)
      .map(([port, value]) => `${port}(${normalizePercent(value, total)})`);
  }

  return [];
}

function normalizeTalkers(payload) {
  const rows =
    payload?.top_ips ||
    payload?.topIps ||
    payload?.top_talkers ||
    payload?.topTalkers ||
    payload?.talkers ||
    payload?.hosts ||
    payload?.connections ||
    [];

  if (!Array.isArray(rows)) {
    return [];
  }

  return rows.slice(0, PAGE_SIZE).map((row, index) => {
    const incoming = positive(row.incoming ?? row.in_packets ?? row.input_packets ?? 0);
    const outgoing = positive(row.outgoing ?? row.out_packets ?? row.output_packets ?? 0);
    const packets = positive(row.packets ?? row.total_packets ?? row.totalPackets ?? incoming + outgoing);
    const bytes = positive(row.bytes ?? row.total_bytes ?? row.totalBytes ?? 0);

    return {
      ip: row.ip || row.address || row.host || row.src_ip || row.source || `Row ${index + 1}`,
      packets,
      bytes,
      incoming,
      outgoing,
      protocols: normalizeProtocols(row),
      ports: normalizePorts(row),
    };
  });
}

function renderDashboard() {
  const stats = state.resetPending ? { ...emptyStats } : state.stats;
  const isPackets = state.metric === "packets";

  elements.incomingRateLabel.textContent = isPackets ? "Incoming Packets / s" : "Incoming Bytes / s";
  elements.outgoingRateLabel.textContent = isPackets ? "Outgoing Packets / s" : "Outgoing Bytes / s";
  elements.incomingTotalLabel.textContent = isPackets ? "Total packets" : "Total bytes";
  elements.outgoingTotalLabel.textContent = isPackets ? "Total packets" : "Total bytes";

  elements.incomingRate.textContent = formatMetricRate(
    isPackets ? stats.incoming_packets_per_second : stats.incoming_bytes_per_second,
  );
  elements.outgoingRate.textContent = formatMetricRate(
    isPackets ? stats.outgoing_packets_per_second : stats.outgoing_bytes_per_second,
  );
  elements.incomingTotal.textContent = formatMetricTotal(
    isPackets ? stats.incoming_packets : stats.incoming_bytes,
  );
  elements.outgoingTotal.textContent = formatMetricTotal(
    isPackets ? stats.outgoing_packets : stats.outgoing_bytes,
  );

  elements.chartTitle.textContent = isPackets ? "Packets Per Second" : "Bytes Per Second";
  elements.packetCounts.tcp_packets.textContent = formatNumber(stats.tcp_packets);
  elements.packetCounts.udp_packets.textContent = formatNumber(stats.udp_packets);
  elements.packetCounts.icmp_packets.textContent = formatNumber(stats.icmp_packets);
  elements.packetCounts.other_packets.textContent = formatNumber(stats.other_packets);
}

function createCell(content, className = "") {
  const cell = document.createElement("td");
  if (className) {
    cell.className = className;
  }

  if (content instanceof Node) {
    cell.appendChild(content);
  } else {
    cell.textContent = content;
  }

  return cell;
}

function renderPills(items) {
  const container = document.createElement("div");
  container.className = "pill-list";

  items.forEach((item) => {
    const pill = document.createElement("span");
    pill.className = "table-pill";
    pill.textContent = item;
    container.appendChild(pill);
  });

  return container;
}

function renderPorts(items) {
  const container = document.createElement("div");
  container.className = "ports-cell";

  items.forEach((item) => {
    const span = document.createElement("span");
    span.textContent = item;
    container.appendChild(span);
  });

  return container;
}

function renderInOut(row) {
  const total = row.incoming + row.outgoing;
  const incomingWidth = total > 0 ? Math.round((row.incoming / total) * 100) : 0;
  const container = document.createElement("div");
  container.className = "inout-cell";
  container.innerHTML = `
    <span>${formatNumber(row.incoming)} / ${formatNumber(row.outgoing)}</span>
    <span class="inout-bar"><span style="width: ${incomingWidth}%"></span></span>
  `;
  return container;
}

function renderActions() {
  const container = document.createElement("div");
  container.className = "actions-cell";

  ["View", "Block"].forEach((label) => {
    const button = document.createElement("button");
    button.className = "row-action";
    button.type = "button";
    button.textContent = label;
    container.appendChild(button);
  });

  return container;
}

function renderTable() {
  const rows = state.resetPending ? [] : state.talkers;
  elements.talkersBody.replaceChildren();

  if (rows.length === 0) {
    const row = document.createElement("tr");
    row.className = "empty-row";
    const cell = document.createElement("td");
    cell.colSpan = 7;
    cell.textContent = "No entries";
    row.appendChild(cell);
    elements.talkersBody.appendChild(row);
    elements.tableSummary.textContent = "Showing 0 to 0 of 0 entries";
    return;
  }

  rows.forEach((talker) => {
    const row = document.createElement("tr");
    row.appendChild(createCell(talker.ip));
    row.appendChild(createCell(formatNumber(talker.packets)));
    row.appendChild(createCell(formatBytes(talker.bytes)));
    row.appendChild(createCell(renderInOut(talker)));
    row.appendChild(createCell(renderPills(talker.protocols.length ? talker.protocols : ["Other 100%"])));
    row.appendChild(createCell(renderPorts(talker.ports)));
    row.appendChild(createCell(renderActions()));
    elements.talkersBody.appendChild(row);
  });

  elements.tableSummary.textContent = `Showing 1 to ${rows.length} of ${rows.length} entries`;
}

function drawGrid(ctx, plot, maxAbs) {
  ctx.save();
  ctx.strokeStyle = "rgba(255, 138, 0, 0.2)";
  ctx.lineWidth = 1;
  ctx.setLineDash([3, 7]);

  [-1, -0.5, 0, 0.5, 1].forEach((ratio) => {
    const value = ratio * maxAbs;
    const y = plot.top + ((maxAbs - value) / (maxAbs * 2)) * plot.height;

    ctx.beginPath();
    ctx.moveTo(plot.left, y);
    ctx.lineTo(plot.left + plot.width, y);
    ctx.stroke();
  });

  ctx.restore();
}

function drawAxes(ctx, plot) {
  ctx.save();
  ctx.strokeStyle = "#ff8a00";
  ctx.lineWidth = 2;
  ctx.setLineDash([]);

  const zeroY = plot.top + plot.height / 2;
  ctx.beginPath();
  ctx.moveTo(plot.left, zeroY);
  ctx.lineTo(plot.left + plot.width, zeroY);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(plot.left, plot.top);
  ctx.lineTo(plot.left, plot.top + plot.height);
  ctx.lineTo(plot.left + plot.width, plot.top + plot.height);
  ctx.stroke();
  ctx.restore();
}

function drawTimeLabels(ctx, plot, startTime, endTime) {
  ctx.save();
  ctx.strokeStyle = "rgba(255, 138, 0, 0.16)";
  ctx.setLineDash([3, 7]);

  const tickInterval = 10 * 1000;
  const firstTick = Math.ceil(startTime / tickInterval) * tickInterval;

  for (let time = firstTick; time <= endTime; time += tickInterval) {
    const ratio = (time - startTime) / (endTime - startTime);
    const x = plot.left + ratio * plot.width;

    ctx.beginPath();
    ctx.moveTo(x, plot.top);
    ctx.lineTo(x, plot.top + plot.height);
    ctx.stroke();
  }

  ctx.restore();
}

function drawSeries(ctx, points, getValue, plot, startTime, endTime, maxAbs, dashed = false) {
  if (points.length === 0) {
    return;
  }

  const xFor = (point) => plot.left + ((point.timeMs - startTime) / (endTime - startTime)) * plot.width;
  const yFor = (value) => plot.top + ((maxAbs - value) / (maxAbs * 2)) * plot.height;

  ctx.save();
  ctx.strokeStyle = "#ff8a00";
  ctx.lineWidth = 2;
  ctx.setLineDash(dashed ? [8, 7] : []);
  ctx.beginPath();

  points.forEach((point, index) => {
    const x = xFor(point);
    const y = yFor(getValue(point));

    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });

  ctx.stroke();
  ctx.restore();
}

function drawChart() {
  if (state.view !== "dashboard") {
    return;
  }

  const canvas = elements.chart;
  const rect = canvas.getBoundingClientRect();

  if (rect.width <= 0 || rect.height <= 0) {
    return;
  }

  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.floor(rect.width * dpr);
  canvas.height = Math.floor(rect.height * dpr);

  const ctx = canvas.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, rect.width, rect.height);

  const plot = {
    left: 34,
    top: 10,
    width: rect.width - 48,
    height: rect.height - 24,
  };
  const points = state.resetPending ? [] : state.history;
  const endTime = Date.now();
  const startTime = endTime - HISTORY_WINDOW_MS;
  const incomingKey = state.metric === "packets" ? "incomingPackets" : "incomingBytes";
  const outgoingKey = state.metric === "packets" ? "outgoingPackets" : "outgoingBytes";
  const maxValue = points.reduce(
    (maximum, point) => Math.max(maximum, point[incomingKey], point[outgoingKey]),
    1,
  );
  const maxAbs = Math.max(1, maxValue * 1.35);

  drawGrid(ctx, plot, maxAbs);
  drawTimeLabels(ctx, plot, startTime, endTime);
  drawAxes(ctx, plot);
  drawSeries(ctx, points, (point) => point[incomingKey], plot, startTime, endTime, maxAbs, false);
  drawSeries(ctx, points, (point) => -point[outgoingKey], plot, startTime, endTime, maxAbs, true);
}

function render() {
  const isOnline = !state.resetPending && state.stats.status === "online";
  elements.statusDiode.classList.toggle("offline", !isOnline);
  elements.viewTitle.textContent = "Traffic Processor";
  elements.lastUpdated.textContent = isOnline ? formatClock(state.stats.timestamp || state.stats._timeMs) : "--:--:--";

  elements.dashboardView.classList.toggle("active", state.view === "dashboard");
  elements.tableView.classList.toggle("active", state.view === "table");
  elements.viewTabs.forEach((button) => {
    button.classList.toggle("active", button.dataset.view === state.view);
  });
  elements.metricButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.metric === state.metric);
  });

  renderDashboard();
  renderTable();
  drawChart();
}

async function loadStats() {
  try {
    const response = await fetch(statsEndpoint, { cache: "no-store" });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    const payload = await response.json();
    const rawStats = normalizeStats(payload);

    const rates = calculateDirectionalRates(rawStats);
    const adjustedStats = { ...rawStats, ...rates };

    state.rawStats = rawStats;
    state.stats = adjustedStats;
    state.talkers = normalizeTalkers(payload);
    state.resetPending = false;
    appendHistory(adjustedStats);
    state.previousRaw = rawStats;
  } catch {
    state.stats = { ...state.stats, status: "offline" };
  }

  render();
}

async function resetDashboard() {
  try {
    const response = await fetch(resetEndpoint, {
      method: "POST",
      cache: "no-store",
    });
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }
  } catch {
    return;
  }

  state.previousRaw = null;
  state.resetPending = true;
  state.stats = { ...emptyStats };
  state.rawStats = null;
  state.history = [];
  state.talkers = [];
  render();

  window.setTimeout(loadStats, POLL_INTERVAL_MS);
}

function exportTalkers() {
  const rows = state.talkers;
  const headers = ["IP", "Packets", "Bytes", "Incoming", "Outgoing", "Protocols", "Ports"];
  const lines = [
    headers.join(","),
    ...rows.map((row) =>
      [
        row.ip,
        row.packets,
        row.bytes,
        row.incoming,
        row.outgoing,
        row.protocols.join(" | "),
        row.ports.join(" | "),
      ]
        .map((value) => `"${String(value).replaceAll('"', '""')}"`)
        .join(","),
    ),
  ];
  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "top-talkers.csv";
  link.click();
  URL.revokeObjectURL(url);
}

elements.viewTabs.forEach((button) => {
  button.addEventListener("click", () => {
    state.view = button.dataset.view;
    render();
  });
});

elements.metricButtons.forEach((button) => {
  button.addEventListener("click", () => {
    state.metric = button.dataset.metric;
    render();
  });
});

elements.resetButton.addEventListener("click", resetDashboard);
elements.refreshButton.addEventListener("click", loadStats);
elements.exportButton.addEventListener("click", exportTalkers);
window.addEventListener("resize", drawChart);

render();
loadStats();

const pollTimer = window.setInterval(loadStats, POLL_INTERVAL_MS);

window.addEventListener("beforeunload", () => {
  window.clearInterval(pollTimer);
});
