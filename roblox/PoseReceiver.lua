-- PoseReceiver (Script / ServerScript)
-- Taruh di: ServerScriptService
--
-- Fungsi: Jembatan antara LocalScript dan relay server
-- LocalScript invoke RemoteFunction ini → server fetch HTTP → balik data

local HttpService = game:GetService("HttpService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- ================================
-- CONFIG
-- URL relay server lo
-- Ganti ke URL server kalau udah di-deploy
-- ================================
local URL = "web-production-7178.up.railway.app"
-- ================================

-- Bikin RemoteFunction kalau belum ada
local getPoseData = ReplicatedStorage:FindFirstChild("GetPoseData")
if not getPoseData then
	getPoseData = Instance.new("RemoteFunction")
	getPoseData.Name = "GetPoseData"
	getPoseData.Parent = ReplicatedStorage
end

getPoseData.OnServerInvoke = function(player)
	local success, result = pcall(function()
		return HttpService:GetAsync(URL)
	end)

	if success then
		local ok, data = pcall(function()
			return HttpService:JSONDecode(result)
		end)
		if ok then return data end
	else
		-- Kalau gagal konek, return idle biar karakter ga error
		return { action = "idle" }
	end

	return { action = "idle" }
end

print("PoseReceiver server ready! Polling:", URL)
